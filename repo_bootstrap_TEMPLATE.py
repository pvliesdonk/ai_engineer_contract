#!/usr/bin/env python3

"""
repo_bootstrap_TEMPLATE.py - Initialize a new GitHub repo with license and CONTRIBUTING
Version: 1.2.0
Generated: 2025-10-14 09:59:08 UTC

USAGE
-----
1) Ensure prerequisites on your machine:
   - git (>= 2.30)
   - GitHub CLI (gh) authenticated (`gh auth status`)
2) Edit the variables below (OWNER, REPO, VISIBILITY, LICENSE_CHOICE, AUTHOR, YEAR).
3) Run:
   python repo_bootstrap_TEMPLATE_v1.2.0.py

It will:
- create a working dir under /mnt/scratch
- if the repo exists, clone it and ensure files exist; otherwise create a new repo
- write LICENSE (MIT/Apache-2.0/Unlicense/None), README.md, CONTRIBUTING.md
- create 'main' and 'develop' branches and push both
- create default labels
"""
from __future__ import annotations
import sys, os, shutil, subprocess, json
from datetime import datetime
from pathlib import Path

# ---- Configuration ----
OWNER = "pvliesdonk"
REPO  = "<REPO_NAME_HERE>"     # <- set me (name only)
VISIBILITY = "public"          # "public" or "private"
LICENSE_CHOICE = "MIT"         # "MIT" | "Apache-2.0" | "Unlicense" | "None"
AUTHOR = "Peter van Liesdonk"  # copyright holder
YEAR = "2025"              # default to current year

LABELS = {
    "from-ai": ("5319e7", "Auto-created label - from AI"),
    "needs-review": ("d93f0b", "Auto-created label - needs review"),
    "blocked": ("b60205", "Auto-created label - blocked"),
    "security": ("000000", "Auto-created label - security"),
    "breaking-change": ("e11d21", "Auto-created label - breaking change"),
    "docs": ("0e8a16", "Auto-created label - documentation"),
    "chore": ("c5def5", "Auto-created label - chore"),
    "content": ("1d76db", "Auto-created label - content"),
    "design": ("fbca04", "Auto-created label - design"),
    "asset": ("bfdadc", "Auto-created label - asset"),
}

SCRATCH = Path("/mnt/scratch")
TS = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
WORKDIR = SCRATCH / f"repo_bootstrap_{OWNER}_{REPO}_{TS}"

# ---- Utilities ----
def run(cmd, cwd=None, check=True):
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise SystemExit(f"ERROR: {cmd}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return p

def ensure_tools():
    for t in ["git", "gh"]:
        p = run([t, "--version"], check=False)
        if p.returncode != 0:
            raise SystemExit(f"ERROR: {t} not found. Please install it.")

def repo_slug():
    if "/" in REPO:
        raise SystemExit("REPO should be name-only (owner is set by OWNER).")
    return f"{OWNER}/{REPO}"

def gh_repo_exists():
    p = run(["gh", "repo", "view", repo_slug()], check=False)
    return p.returncode == 0

def ensure_labels(cwd):
    p = run(["gh", "label", "list", "--json", "name"], cwd=cwd, check=False)
    existing = set()
    if p.returncode == 0 and p.stdout.strip():
        try:
            data = json.loads(p.stdout)
            existing = {it["name"] for it in data if "name" in it}
        except Exception:
            existing = {line.split()[0] for line in p.stdout.splitlines() if line.strip()}
    for name, (color, desc) in LABELS.items():
        if name in existing:
            continue
        r = run(["gh", "label", "create", name, "--color", color, "--description", desc], cwd=cwd, check=False)
        if r.returncode != 0:
            print(f"WARNING: failed to create label '{name}':\n{r.stderr or r.stdout}", file=sys.stderr)

# ---- Content ----

def mit_text(year: str, author: str) -> str:
    return f"""MIT License

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
"""

APACHE2_SNIPPET = """Apache License, Version 2.0 (January 2004)
See http://www.apache.org/licenses/LICENSE-2.0
Paste the full Apache-2.0 text here if your project requires it.
"""

UNLICENSE = """This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors of
this software dedicate any and all copyright interest in the software to
the public domain. We make this dedication for the benefit of the public
at large and to the detriment of our heirs and successors. We intend
this dedication to be an overt act of relinquishment in perpetuity of
all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

def readme_text(owner: str, repo: str) -> str:
    return f"""# {repo}

Short description of the project.

## Getting Started

- Clone: `gh repo clone {owner}/{repo}`
- Read [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow.
"""

CONTRIBUTING = """# Contributing

This repository follows the AI x Peter Engineering Contract & Working Agreement.

## Workflow (TL;DR)
- Base your work on the latest `origin/develop`.
- Create a feature/fix branch: `feat/<slug>` / `fix/<slug>` / `docs/<slug>` / `chore/<slug>`.
- Use Conventional Commits for the PR title (squash merge preserves it).
- Open a PR into `develop` with the PR body template:
  - Summary, Why, Changes, Validation, Risk & Rollback, Notes for Reviewer.
- Labels: `from-ai`, `needs-review`, plus any relevant (`docs`, `content`, `design`, `asset`, etc.).

## Validation
- Keep PRs small and self-contained.
- Include commands or steps to reproduce results (build/test/preview).

For full details, see the contract in the project prompt or repository docs.
"""

GITIGNORE = """.DS_Store
.env
venv/
__pycache__/
node_modules/
dist/
build/
"""

def write_if_missing(path: Path, content: str):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

def main():
    # Basic input checks
    if REPO == "<REPO_NAME_HERE>":
        raise SystemExit("Please set REPO to your repository name.")
    if VISIBILITY not in ("public", "private"):
        raise SystemExit("VISIBILITY must be 'public' or 'private'.")

    # Tools
    for t in ("git", "gh"):
        p = subprocess.run([t, "--version"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode != 0:
            raise SystemExit(f"ERROR: {t} not found.")

    # Workspace
    SCRATCH.mkdir(parents=True, exist_ok=True)
    if WORKDIR.exists():
        shutil.rmtree(WORKDIR)
    WORKDIR.mkdir()

    # If repo exists, clone; else init new and create remote
    slug = f"{OWNER}/{REPO}"
    p = subprocess.run(["gh", "repo", "view", slug], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode == 0:
        subprocess.run(["gh", "repo", "clone", slug, str(WORKDIR)], check=True, text=True)
        cwd = WORKDIR
        subprocess.run(["git", "checkout", "main"], cwd=cwd, check=False, text=True)
    else:
        cwd = WORKDIR
        subprocess.run(["git", "init", "-b", "main"], cwd=cwd, check=True, text=True)
        # LICENSE
        if LICENSE_CHOICE == "MIT":
            write_if_missing(cwd / "LICENSE", mit_text(YEAR, AUTHOR))
        elif LICENSE_CHOICE == "Apache-2.0":
            write_if_missing(cwd / "LICENSE", APACHE2_SNIPPET)
        elif LICENSE_CHOICE == "Unlicense":
            write_if_missing(cwd / "LICENSE", UNLICENSE)
        # Other files
        write_if_missing(cwd / "README.md", readme_text(OWNER, REPO))
        write_if_missing(cwd / "CONTRIBUTING.md", CONTRIBUTING)
        write_if_missing(cwd / ".gitignore", GITIGNORE)
        # Commit
        subprocess.run(["git", "add", "-A"], cwd=cwd, check=True, text=True)
        subprocess.run(["git", "commit", "-m", f"chore: bootstrap repository (license: {LICENSE_CHOICE})"], cwd=cwd, check=True, text=True)
        # Create remote and push
        vis_flag = "--public" if VISIBILITY == "public" else "--private"
        subprocess.run(["gh", "repo", "create", slug, vis_flag, "--source", str(cwd), "--remote", "origin", "--push"], cwd=cwd, check=True, text=True)

    # Ensure develop branch exists and is pushed
    subprocess.run(["git", "checkout", "main"], cwd=cwd, check=False, text=True)
    subprocess.run(["git", "checkout", "-B", "develop"], cwd=cwd, check=True, text=True)
    subprocess.run(["git", "push", "-u", "origin", "develop"], cwd=cwd, check=True, text=True)

    # Ensure labels
    ensure_labels(cwd)

    print(f"SUCCESS: Repository initialized at {slug}.")
    print(f"Local working copy: {cwd}")

if __name__ == "__main__":
    main()
