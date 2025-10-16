#!/usr/bin/env python3
# Intent: Template script to bootstrap a new repository with main + develop branches,
# labels, LICENSE/README/CONTRIBUTING. Tool-agnostic; adapt to your org's defaults.
from __future__ import annotations
import subprocess, sys, json
from pathlib import Path

OWNER="pvliesdonk"; REPO="<REPO_NAME_HERE>"; VISIBILITY="public"
LICENSE="MIT"

def run(cmd, cwd=None):
    p=subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode!=0: sys.exit(p.stderr or "command failed")
    return p.stdout

def main():
    # requires authenticated gh
    run(["gh","repo","create",f"{OWNER}/{REPO}","--"+VISIBILITY,"--confirm"])
    run(["gh","repo","clone",f"{OWNER}/{REPO}",REPO])
    repo=Path(REPO)
    (repo/".gitignore").write_text(".venv/\n.DS_Store\n__pycache__/\n", encoding="utf-8")
    (repo/"README.md").write_text(f"# {REPO}\n", encoding="utf-8")
    (repo/"CONTRIBUTING.md").write_text("# Contributing\n", encoding="utf-8")
    # default branch main; create develop
    run(["git","-C",str(repo),"checkout","-b","develop"])
    run(["git","-C",str(repo),"commit","--allow-empty","-m","chore: initialize develop"])
    run(["git","-C",str(repo),"push","-u","origin","develop"])
    # labels
    labels={"from-ai":"5319e7","needs-review":"d93f0b","docs":"0e8a16","chore":"c5def5","security":"000000","blocked":"b60205","planning":"0052cc","needs-design-ref":"1d76db","breaking-change":"e11d21","content":"1d76db","design":"fbca04","asset":"bfdadc","deviation-approved":"5319e7"}
    for name,color in labels.items():
        subprocess.run(["gh","label","create",name,"--color",color,"--description",f"Auto-created label - {name}"], cwd=str(repo), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Repo bootstrap complete")

if __name__=="__main__": main()
