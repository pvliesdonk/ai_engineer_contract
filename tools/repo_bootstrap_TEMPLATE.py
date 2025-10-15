#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, shutil, subprocess
from datetime import datetime
from pathlib import Path

OWNER = "pvliesdonk"
REPO  = "<REPO_NAME_HERE>"
VISIBILITY = "public"          # or "private"
LICENSE_CHOICE = "MIT"         # "MIT" | "Apache-2.0" | "Unlicense" | "None"
AUTHOR = "Peter van Liesdonk"
YEAR = datetime.utcnow().strftime("%Y")

LABELS = {
    "from-ai": ("5319e7","Auto-created label - from AI"),
    "needs-review": ("d93f0b","Auto-created label - needs review"),
    "blocked": ("b60205","Auto-created label - blocked"),
    "security": ("000000","Auto-created label - security"),
    "breaking-change": ("e11d21","Auto-created label - breaking change"),
    "docs": ("0e8a16","Auto-created label - documentation"),
    "chore": ("c5def5","Auto-created label - chore"),
    "content": ("1d76db","Auto-created label - content"),
    "design": ("fbca04","Auto-created label - design"),
    "asset": ("bfdadc","Auto-created label - asset"),
    "deviation-approved": ("5319e7","Auto-created label - deviation approved"),
}

SCRATCH = Path("/mnt/scratch")
TS = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
WORKDIR = SCRATCH / f"repo_bootstrap_{OWNER}_{REPO}_{TS}"

def run(cmd, cwd=None, check=True):
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise SystemExit(f"ERROR: {cmd}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return p

def write_if_missing(path: Path, content: str):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

def mit_text(year: str, author: str) -> str:
    return f\"\"\"MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
\"\"\"

APACHE2_SNIPPET = "Apache License 2.0 - see http://www.apache.org/licenses/LICENSE-2.0"
UNLICENSE = "Unlicense - see https://unlicense.org/"

def main():
    parser=argparse.ArgumentParser(description="Create or normalize a repository.")
    parser.add_argument("--owner", default=OWNER)
    parser.add_argument("--repo", default=REPO, help="name-only")
    parser.add_argument("--visibility", default=VISIBILITY, choices=["public","private"])
    parser.add_argument("--license", default=LICENSE_CHOICE, choices=["MIT","Apache-2.0","Unlicense","None"])
    parser.add_argument("--author", default=AUTHOR)
    parser.add_argument("--base-branch", default=os.environ.get("BASE_BRANCH","develop"))
    args=parser.parse_args()

    owner, repo = args.owner, args.repo
    dev_branch = args.base_branch

    for t in ("git","gh"):
        if run([t,"--version"],check=False).returncode!=0: raise SystemExit(f"ERROR: {t} not found.")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    if WORKDIR.exists(): shutil.rmtree(WORKDIR)
    WORKDIR.mkdir()

    slug=f"{owner}/{repo}"
    if run(["gh","repo","view",slug],check=False).returncode==0:
        run(["gh","repo","clone",slug,str(WORKDIR)])
        cwd=WORKDIR
        run(["git","checkout","main"],cwd=cwd,check=False)
    else:
        cwd=WORKDIR
        run(["git","init","-b","main"],cwd=cwd)
        if args.license=="MIT": write_if_missing(cwd/"LICENSE", mit_text(YEAR, args.author))
        elif args.license=="Apache-2.0": write_if_missing(cwd/"LICENSE", APACHE2_SNIPPET)
        elif args.license=="Unlicense": write_if_missing(cwd/"LICENSE", UNLICENSE)
        write_if_missing(cwd/"README.md", f"# {repo}\n")
        write_if_missing(cwd/"CONTRIBUTING.md", "# Contributing\n\nSee ENGINEERING_CONTRACT.md (canonical).\n")
        write_if_missing(cwd/".gitignore",".DS_Store\n.env\n")
        run(["git","add","-A"],cwd=cwd); run(["git","commit","-m",f"chore: bootstrap repository (license: {args.license})"],cwd=cwd)
        vis_flag="--public" if args.visibility=="public" else "--private"
        run(["gh","repo","create",slug,vis_flag,"--source",str(cwd),"--remote","origin","--push"],cwd=cwd)

    run(["git","checkout","main"],cwd=cwd,check=False)
    run(["git","checkout","-B",dev_branch],cwd=cwd)
    run(["git","push","-u","origin",dev_branch],cwd=cwd)

    p=run(["gh","label","list","--json","name"],cwd=cwd,check=False)
    existing=set()
    if p.returncode==0 and p.stdout.strip():
        try: existing={it["name"] for it in json.loads(p.stdout) if "name" in it}
        except Exception: existing={ln.split()[0] for ln in p.stdout.splitlines() if ln.strip()}
    for name,(color,desc) in LABELS.items():
        if name in existing: continue
        run(["gh","label","create",name,"--color",color,"--description",desc],cwd=cwd,check=False)

    print(f"SUCCESS: Repository initialized at {slug}. Development branch: {dev_branch}")
    print(f"Local working copy: {cwd}")

if __name__=="__main__": main()
