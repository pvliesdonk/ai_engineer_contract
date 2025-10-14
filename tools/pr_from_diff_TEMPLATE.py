#!/usr/bin/env python3
from __future__ import annotations
import base64, hashlib, os, shutil, subprocess, sys, json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

OWNER = "pvliesdonk"
REPO  = "<REPO_NAME_HERE>"
BASE_BRANCH = os.environ.get("BASE_BRANCH", "develop")
PR_TITLE = "feat: <edit me> short, imperative summary"
PR_BODY  = "# Summary\n<why/changes/validation/risk>"
BRANCH_NAME = ""
DIFF_CONTENT = r""
DIFF_B64 = ""
DIFF_SHA256 = ""
FILE_BLOBS: Dict[str, str] = {}
PR_LABELS = ["from-ai", "needs-review"]
LABEL_COLORS = {"from-ai":"5319e7","needs-review":"d93f0b","blocked":"b60205","security":"000000","breaking-change":"e11d21","docs":"0e8a16","chore":"c5def5","content":"1d76db","design":"fbca04","asset":"bfdadc"}
PR_REVIEWERS: List[str] = []

SCRATCH_DIR = Path("/mnt/scratch")
TIMESTAMP = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
WORKDIR = SCRATCH_DIR / f"pr_work_{OWNER}_{REPO}_{TIMESTAMP}"

@dataclass
class CmdResult:
    code: int
    out: str
    err: str

def run(cmd: List[str], cwd: Optional[Path]=None, check=False)->CmdResult:
    p=subprocess.run(cmd,cwd=str(cwd) if cwd else None,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if check and p.returncode!=0:
        raise RuntimeError(f"Command failed: {cmd}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return CmdResult(p.returncode,p.stdout,p.stderr)

def ensure_tools():
    for t in ["git","gh"]:
        if run([t,"--version"]).code!=0:
            sys.exit(f"ERROR: {t} not found.")

def repo_slug()->str:
    if "/" in REPO:
        sys.exit("ERROR: REPO must be name-only, not owner/name.")
    return f"{OWNER}/{REPO}"

def gh_repo_exists()->bool:
    return run(["gh","repo","view",repo_slug()]).code==0

def clone_repo():
    WORKDIR.parent.mkdir(parents=True,exist_ok=True)
    if WORKDIR.exists():
        shutil.rmtree(WORKDIR)
    r=run(["gh","repo","clone",repo_slug(),str(WORKDIR)])
    if r.code!=0:
        sys.exit(f"ERROR: clone failed\n{r.err or r.out}")

def prepare_branch()->str:
    for c in (["git","fetch","--all","--prune"],
              ["git","checkout",BASE_BRANCH],
              ["git","reset","--hard",f"origin/{BASE_BRANCH}"]):
        r=run(c,cwd=WORKDIR)
        if r.code!=0:
            sys.exit(f"ERROR: {' '.join(c)}\n{r.err or r.out}")
    import re
    slug=re.sub(r"[^a-z0-9]+","-",PR_TITLE.lower()).strip("-") or "changes"
    branch=(BRANCH_NAME.strip() or f"ai/{slug[:40]}-{TIMESTAMP}")
    if run(["git","switch","-c",branch],cwd=WORKDIR).code!=0:
        sys.exit(f"ERROR: switch {branch}")
    return branch

def ensure_labels():
    r=run(["gh","label","list","--json","name"],cwd=WORKDIR)
    existing=set()
    if r.code==0 and r.out.strip():
        try:
            existing={x["name"] for x in json.loads(r.out)}
        except Exception:
            existing={ln.split()[0] for ln in r.out.splitlines() if ln.strip()}
    for name in PR_LABELS:
        if name in existing:
            continue
        color=LABEL_COLORS.get(name,"bfdadc")
        rr=run(["gh","label","create",name,"--color",color,"--description",f"Auto-created label - {name}"],cwd=WORKDIR)
        if rr.code!=0:
            print(f"WARNING: label create '{name}':\n{rr.err or rr.out}",file=sys.stderr)

def normalized_diff_bytes()->bytes:
    if DIFF_B64.strip():
        d=base64.b64decode(DIFF_B64)
        if DIFF_SHA256 and hashlib.sha256(d).hexdigest().lower()!=DIFF_SHA256.lower():
            sys.exit("ERROR: DIFF_SHA256 mismatch")
        return d.replace(b"\r\n",b"\n")
    elif DIFF_CONTENT.strip():
        return DIFF_CONTENT.replace("\r\n","\n").encode("utf-8")
    return b""

def apply_diff_and_blobs():
    d=normalized_diff_bytes()
    if d:
        df=WORKDIR/"changes.diff"
        df.write_bytes(d)
        if run(["git","apply","--index","--whitespace=fix",str(df)],cwd=WORKDIR).code!=0:
            if run(["patch","-p1","-N","-r","rejections.log","-i",str(df)],cwd=WORKDIR).code!=0:
                sys.exit("ERROR: cannot apply diff")
    elif not FILE_BLOBS:
        sys.exit("ERROR: no changes to apply")
    for path,b64 in FILE_BLOBS.items():
        p=(WORKDIR/path)
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(base64.b64decode(b64))
        if run(["git","add",path],cwd=WORKDIR).code!=0:
            sys.exit(f"ERROR: git add {path}")

def commit_and_push(branch:str):
    run(["git","add","-A"],cwd=WORKDIR)
    if run(["git","status","--porcelain"],cwd=WORKDIR).out.strip()=="":
        sys.exit("ERROR: no staged changes")
    if run(["git","commit","-m",PR_TITLE],cwd=WORKDIR).code!=0:
        sys.exit("ERROR: commit failed")
    if run(["git","push","-u","origin",branch],cwd=WORKDIR).code!=0:
        sys.exit("ERROR: push failed")

def create_pr(branch:str):
    args=["gh","pr","create","--base",BASE_BRANCH,"--head",branch,"--title",PR_TITLE,"--body",PR_BODY]
    for lab in PR_LABELS:
        args+=["--label",lab]
    if PR_REVIEWERS:
        args+=["--reviewer",",".join(PR_REVIEWERS)]
    r=run(args,cwd=WORKDIR)
    if r.code!=0:
        sys.exit(f"ERROR: gh pr create\n{r.err or r.out}")
    print(r.out.strip())

def main():
    ensure_tools()
    SCRATCH_DIR.mkdir(parents=True,exist_ok=True)
    if not gh_repo_exists():
        sys.exit(f"ERROR: repo '{repo_slug()}' not accessible")
    clone_repo()
    branch=prepare_branch()
    ensure_labels()
    apply_diff_and_blobs()
    commit_and_push(branch)
    create_pr(branch)
    print(f"SUCCESS: Opened PR from '{branch}' into '{BASE_BRANCH}' for {repo_slug()}")

if __name__=="__main__":
    main()
