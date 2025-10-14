#!/usr/bin/env python3

"""
pr_from_diff_TEMPLATE.py — Create a GitHub PR from an embedded unified diff
Version: 1.0.0
Generated: 2025-10-14 08:48:39 UTC

USAGE
-----
1) Ensure prerequisites on your machine:
   - git (>= 2.30)
   - GitHub CLI (gh) authenticated for Git operations (`gh auth status`)
2) Edit this file to set:
   - OWNER = "pvliesdonk"
   - REPO = "<your-repo-name>"
   - PR_TITLE, PR_BODY
   - BRANCH_NAME (optional; will auto-generate if empty)
   - DIFF_CONTENT (paste a valid unified diff)
   - Optional: FILE_BLOBS for adding new files via base64 (text or binary)
3) Run:
   python pr_from_diff_TEMPLATE.py

The script will:
- clone the repo to /mnt/scratch/…
- create a branch from origin/develop
- apply the embedded diff (and optional file blobs)
- commit, push, and open a PR against develop

NOTES
-----
- The DIFF must be a valid *unified diff* against the current origin/develop.
- If your change introduces new files, prefer including them in the diff.
  For binaries or when diff is inconvenient, place base64 in FILE_BLOBS.
- The script is intentionally strict; failures abort with a helpful message.

LICENSE
-------
Public domain / CC0. Adapt as needed.
"""

from __future__ import annotations
import base64
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

OWNER = "pvliesdonk"
REPO  = "<REPO_NAME_HERE>"  # TODO: set your repository name (no owner)
BASE_BRANCH = "develop"     # PR base
PR_TITLE = "feat: <edit me> short, imperative summary"
PR_BODY  = """
# Summary
Explain what/why in 2–4 sentences.

# Changes
- Itemized list

# Validation
- Commands/screenshots

# Risk & Rollback
- Expected impact; how to revert quickly
""".strip()

# Optional: give your branch a predictable name; otherwise auto-slugged.
BRANCH_NAME = ""  # e.g., "feat/config-loader"

# Paste a valid unified diff between the triple quotes. Leave empty to abort.
DIFF_CONTENT = r"""
# --- PASTE YOUR UNIFIED DIFF HERE ---
# Example (remove this example when pasting real diff):
# diff --git a/README.md b/README.md
# index e69de29..4b825dc 100644
# --- a/README.md
# +++ b/README.md
# @@
# +# Project
# +Temporary demo line added by pr_from_diff_TEMPLATE.py
"""

# Optional file blobs: map of repo-relative path -> base64-encoded file content.
# If DIFF_CONTENT already covers new files, you probably don't need this.
FILE_BLOBS = {}
# Example:
# FILE_BLOBS = {
#   "docs/new_diagram.png": "<base64…>",
#   "examples/seed.txt": base64.b64encode(b"hello\n").decode("ascii"),
# }

# Labels and reviewers are optional. Adjust to your workflow.
PR_LABELS = ["from-ai", "needs-review"]
PR_REVIEWERS = []  # GitHub usernames, e.g., ["pvliesdonk"]

SCRATCH_DIR = Path("/mnt/scratch")
TIMESTAMP = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
WORKDIR = SCRATCH_DIR / f"pr_work_{OWNER}_{REPO}_{TIMESTAMP}"

# -------- Helpers --------

@dataclass
class CmdResult:
    code: int
    out: str
    err: str

def run(cmd: List[str], cwd: Optional[Path] = None, check: bool = False) -> CmdResult:
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return CmdResult(p.returncode, p.stdout, p.stderr)

def ensure_tools():
    for tool in ["git", "gh"]:
        r = run([tool, "--version"])
        if r.code != 0:
            sys.exit(f"ERROR: {tool} not found or not executable. Install it first.")

def repo_slug() -> str:
    if "/" in REPO:
        sys.exit("ERROR: REPO should be name-only (owner is set by OWNER).")
    return f"{OWNER}/{REPO}"

def gh_repo_exists() -> bool:
    r = run(["gh", "repo", "view", repo_slug()])
    return r.code == 0

def clone_repo():
    WORKDIR.parent.mkdir(parents=True, exist_ok=True)
    if WORKDIR.exists():
        shutil.rmtree(WORKDIR)
    r = run(["gh", "repo", "clone", repo_slug(), str(WORKDIR)])
    if r.code != 0:
        sys.exit(f"ERROR: failed to clone repo {repo_slug()}\n{r.err or r.out}")

def prepare_branch() -> str:
    # Checkout and sync base
    r = run(["git", "fetch", "--all", "--prune"], cwd=WORKDIR)
    if r.code != 0:
        sys.exit(f"ERROR: git fetch failed\n{r.err or r.out}")

    r = run(["git", "checkout", BASE_BRANCH], cwd=WORKDIR)
    if r.code != 0:
        sys.exit(f"ERROR: base branch '{BASE_BRANCH}' not found locally.\n{r.err or r.out}")

    r = run(["git", "reset", "--hard", f"origin/{BASE_BRANCH}"], cwd=WORKDIR)
    if r.code != 0:
        sys.exit(f"ERROR: failed to reset to origin/{BASE_BRANCH}\n{r.err or r.out}")

    # Create branch
    branch = BRANCH_NAME.strip() or auto_branch_name(PR_TITLE)
    r = run(["git", "switch", "-c", branch], cwd=WORKDIR)
    if r.code != 0:
        sys.exit(f"ERROR: could not create/switch to branch '{branch}'\n{r.err or r.out}")
    return branch

def auto_branch_name(title: str) -> str:
    import re
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    if not slug:
        slug = "changes"
    return f"ai/{slug[:40]}-{TIMESTAMP}"

def apply_diff_and_blobs():
    if DIFF_CONTENT.strip() and not DIFF_CONTENT.strip().startswith("# --- PASTE"):
        diff_file = WORKDIR / "changes.diff"
        diff_file.write_text(DIFF_CONTENT, encoding="utf-8")
        r = run(["git", "apply", "--index", "--whitespace=fix", str(diff_file)], cwd=WORKDIR)
        if r.code != 0:
            # Try with patch as a fallback (can be more tolerant)
            r2 = run(["patch", "-p1", "-N", "-r", "rejections.log"], cwd=WORKDIR)
            if r2.code != 0:
                sys.exit("ERROR: failed to apply diff via git apply and patch.\n"
                         f"git apply:\n{r.err or r.out}\npatch:\n{r2.err or r2.out}")
    else:
        # No diff? If no file blobs either, abort.
        if not FILE_BLOBS:
            sys.exit("ERROR: No DIFF_CONTENT provided and FILE_BLOBS is empty. "
                     "Edit this script and paste a unified diff in DIFF_CONTENT.")
    # Write file blobs if any
    for path, b64 in FILE_BLOBS.items():
        target = WORKDIR / path
        target.parent.mkdir(parents=True, exist_ok=True)
        data = base64.b64decode(b64.encode("ascii"))
        target.write_bytes(data)
        r = run(["git", "add", path], cwd=WORKDIR)
        if r.code != 0:
            sys.exit(f"ERROR: git add failed for {path}\n{r.err or r.out}")

def commit_and_push(branch: str):
    # Ensure new/modified files are staged
    run(["git", "add", "-A"], cwd=WORKDIR)
    r = run(["git", "status", "--porcelain"], cwd=WORKDIR)
    if r.code != 0:
        sys.exit(f"ERROR: git status failed\n{r.err or r.out}")
    if not r.out.strip():
        sys.exit("ERROR: No changes to commit after applying diff/blobs. "
                 "Is the diff up-to-date with origin/develop?")

    r = run(["git", "commit", "-m", PR_TITLE], cwd=WORKDIR)
    if r.code != 0:
        sys.exit(f"ERROR: git commit failed\n{r.err or r.out}")

    r = run(["git", "push", "-u", "origin", branch], cwd=WORKDIR)
    if r.code != 0:
        sys.exit(f"ERROR: git push failed\n{r.err or r.out}")

def create_pr(branch: str):
    # Build CLI args
    args = ["gh", "pr", "create", "--base", BASE_BRANCH, "--head", branch,
            "--title", PR_TITLE, "--body", PR_BODY]
    for label in PR_LABELS:
        args += ["--label", label]
    if PR_REVIEWERS:
        args += ["--reviewer", ",".join(PR_REVIEWERS)]
    r = run(args, cwd=WORKDIR)
    if r.code != 0:
        sys.exit(f"ERROR: gh pr create failed\n{r.err or r.out}")
    print(r.out.strip())

def main():
    ensure_tools()
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    if not gh_repo_exists():
        sys.exit(f"ERROR: GitHub repo '{repo_slug()}' does not exist or is inaccessible. "
                 f"Create it first (e.g., `gh repo create {repo_slug()} --public`).")
    clone_repo()
    branch = prepare_branch()
    apply_diff_and_blobs()
    commit_and_push(branch)
    create_pr(branch)
    print(f"SUCCESS: Opened PR from '{branch}' into '{BASE_BRANCH}' for {repo_slug()}")

if __name__ == "__main__":
    main()
