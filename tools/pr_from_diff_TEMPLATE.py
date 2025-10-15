#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, hashlib, json, os, shutil, subprocess, sys, re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

OWNER = "pvliesdonk"
REPO  = "<REPO_NAME_HERE>"         # name-only; override with --repo
PR_TITLE = "feat: <edit me> short, imperative summary"
PR_BODY  = "# Summary\n<why/changes/validation/risk>"
BRANCH_NAME = ""                   # auto if empty
DIFF_CONTENT = r""                 # raw unified diff (utf-8)
DIFF_B64 = ""                      # base64-encoded diff
DIFF_SHA256 = ""                   # optional integrity check of DIFF_B64
FILE_BLOBS: Dict[str, str] = {}    # {"path": base64-content}
PR_LABELS = ["from-ai", "needs-review"]
LABEL_COLORS = {"from-ai":"5319e7","needs-review":"d93f0b","blocked":"b60205","security":"000000","breaking-change":"e11d21","docs":"0e8a16","chore":"c5def5","content":"1d76db","design":"fbca04","asset":"bfdadc","deviation-approved":"5319e7"}
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

def repo_slug(repo: str)->str:
    if "/" in repo:
        sys.exit("ERROR: REPO must be name-only, not owner/name.")
    return f"{OWNER}/{repo}"

def gh_repo_exists(repo: str)->bool:
    return run(["gh","repo","view",repo_slug(repo)]).code==0

def clone_repo(repo: str):
    WORKDIR.parent.mkdir(parents=True,exist_ok=True)
    if WORKDIR.exists():
        shutil.rmtree(WORKDIR)
    r=run(["gh","repo","clone",repo_slug(repo),str(WORKDIR)])
    if r.code!=0:
        sys.exit(f"ERROR: clone failed\n{r.err or r.out}")

def prepare_branch(base_branch: str)->str:
    for c in (["git","fetch","--all","--prune"],
              ["git","checkout",base_branch],
              ["git","reset","--hard",f"origin/{base_branch}"]):
        r=run(c,cwd=WORKDIR)
        if r.code!=0:
            sys.exit(f"ERROR: {' '.join(c)}\n{r.err or r.out}")
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
            if run(["patch","-","-p1","-N","-r","rejections.log"],cwd=WORKDIR).code==0:
                pass
            else:
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

def create_pr(base_branch:str, branch:str):
    args=["gh","pr","create","--base",base_branch,"--head",branch,"--title",PR_TITLE,"--body",PR_BODY]
    for lab in PR_LABELS:
        args+=["--label",lab]
    if PR_REVIEWERS:
        args+=["--reviewer",",".join(PR_REVIEWERS)]
    r=run(args,cwd=WORKDIR)
    if r.code!=0:
        sys.exit(f"ERROR: gh pr create\n{r.err or r.out}")
    print(r.out.strip())

def main():
    parser=argparse.ArgumentParser(description="Create a PR from embedded diff or blobs.")
    parser.add_argument("--owner", default=OWNER)
    parser.add_argument("--repo", default=REPO, help="name-only")
    parser.add_argument("--base-branch", default=os.environ.get("BASE_BRANCH","develop"))
    parser.add_argument("--dry-run", action="store_true")
    args=parser.parse_args()

    global OWNER, REPO
    OWNER, REPO = args.owner, (args.repo or REPO)

    ensure_tools()
    if not gh_repo_exists(REPO):
        sys.exit(f"ERROR: repo '{repo_slug(REPO)}' not accessible")
    if args.dry_run:
        print("DRY-RUN PLAN")
        print(f"- Repo: {repo_slug(REPO)}")
        print(f"- Base branch: {args.base-branch if hasattr(args,'base-branch') else args.base_branch}")
        print(f"- PR title: {PR_TITLE}")
        print(f"- Labels: {PR_LABELS}")
        print(f"- Diff bytes: {len(normalized_diff_bytes())}")
        print(f"- File blobs: {list(FILE_BLOBS.keys())}")
        return

    clone_repo(REPO)
    branch=prepare_branch(args.base_branch)
    ensure_labels()
    apply_diff_and_blobs()
    commit_and_push(branch)
    create_pr(args.base_branch, branch)
    print(f"SUCCESS: Opened PR from '{branch}' into '{args.base_branch}' for {repo_slug(REPO)}")

if __name__=="__main__":
    main()
