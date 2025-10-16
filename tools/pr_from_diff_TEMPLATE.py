#!/usr/bin/env python3
# Intent: Template script to open a PR against 'develop' using a provided diff or file blobs.
# Tool-agnostic by design; expects authenticated gh + git when used as-is.
from __future__ import annotations
import argparse, base64, json, os, re, subprocess, sys
from pathlib import Path
from datetime import datetime

OWNER="pvliesdonk"; REPO="<REPO_NAME_HERE>"
BASE_BRANCH="develop"
PR_TITLE="feat: <edit me>"; PR_BODY="# Summary\n<why/changes/validation/risk>"
PR_LABELS=["from-ai","needs-review"]
LABEL_COLORS={"from-ai":"5319e7","needs-review":"d93f0b","docs":"0e8a16","chore":"c5def5","security":"000000","blocked":"b60205","breaking-change":"e11d21","content":"1d76db","design":"fbca04","asset":"bfdadc","deviation-approved":"5319e7"}
DIFF_B64=""; DIFF_CONTENT=r""; FILE_BLOBS={}
SCRATCH=Path("/mnt/scratch"); TS=datetime.utcnow().strftime("%Y%m%d_%H%M%S")

def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def repo_slug(owner, repo): return f"{owner}/{repo}"

def ensure_tools():
    for t in ("git","gh"):
        if run([t,"--version"]).returncode!=0:
            sys.exit(f"ERROR: {t} not found")

def normalized_diff():
    data = (base64.b64decode(DIFF_B64) if DIFF_B64 else DIFF_CONTENT.encode())
    return data.replace(b"\r\n", b"\n")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--owner",default=OWNER); ap.add_argument("--repo",default=REPO)
    ap.add_argument("--dry-run",action="store_true")
    a=ap.parse_args()

    ensure_tools()
    if run(["gh","repo","view",repo_slug(a.owner,a.repo)]).returncode!=0:
        sys.exit("ERROR: cannot view repo (check auth/permissions)")

    if a.dry_run:
        print("DRY-RUN OK", a.repo, BASE_BRANCH, PR_TITLE, list(FILE_BLOBS)); return

    work=SCRATCH/f"pr_{a.owner}_{a.repo}_{TS}"; work.mkdir(parents=True, exist_ok=True)
    if run(["gh","repo","clone",repo_slug(a.owner,a.repo),str(work)]).returncode!=0: sys.exit("clone failed")
    for c in (["git","fetch","--all","--prune"],["git","checkout",BASE_BRANCH],["git","reset","--hard",f"origin/{BASE_BRANCH}"]):
        if run(c, cwd=str(work)).returncode!=0: sys.exit("git prep failed")

    slug=re.sub(r"[^a-z0-9]+","-",PR_TITLE.lower()).strip("-") or "changes"
    branch=f"ai/{slug[:40]}-{TS}"
    if run(["git","switch","-c",branch], cwd=str(work)).returncode!=0: sys.exit("branch create failed")

    # ensure labels
    existing=set()
    out=run(["gh","label","list","--json","name"], cwd=str(work)).stdout
    try:
        existing={x["name"] for x in json.loads(out)} if out else set()
    except Exception:
        existing=set()
    for lab in PR_LABELS:
        if lab not in existing:
            col=LABEL_COLORS.get(lab,"bfdadc")
            run(["gh","label","create",lab,"--color",col,"--description",f"Auto-created label - {lab}"], cwd=str(work))

    changed=False
    if DIFF_B64 or DIFF_CONTENT:
        df=work/"changes.diff"; df.write_bytes(normalized_diff())
        if run(["git","apply","--index","--whitespace=fix",str(df)], cwd=str(work)).returncode!=0: sys.exit("apply diff failed")
        changed=True

    for path,b64 in FILE_BLOBS.items():
        p=work/path; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(base64.b64decode(b64))
        run(["git","add",path], cwd=str(work)); changed=True

    if not changed: sys.exit("no changes to commit")
    if run(["git","commit","-m",PR_TITLE], cwd=str(work)).returncode!=0: sys.exit("commit failed")
    if run(["git","push","-u","origin",branch], cwd=str(work)).returncode!=0: sys.exit("push failed")

    args=["gh","pr","create","--base",BASE_BRANCH,"--head",branch,"--title",PR_TITLE,"--body",PR_BODY]
    for lab in PR_LABELS: args+=["--label",lab]
    r=run(args, cwd=str(work))
    if r.returncode!=0: sys.exit("pr create failed")
    print(r.stdout.strip())

if __name__=="__main__": main()
