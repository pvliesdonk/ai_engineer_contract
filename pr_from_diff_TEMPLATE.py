#!/usr/bin/env python3
"""
pr_from_diff_TEMPLATE.py — Create a GitHub PR from an embedded unified diff
Version: 1.1.0
Generated: 2025-10-14 09:40:21 UTC

USAGE
-----
1) Prereqs on your machine:
   - git (>= 2.30)
   - GitHub CLI (gh) authenticated for Git operations (`gh auth status`)
2) Edit this file to set:
   - OWNER = "pvliesdonk"
   - REPO = "<your-repo-name>"
   - PR_TITLE, PR_BODY
   - BRANCH_NAME (optional; will auto-generate if empty)
   - DIFF_CONTENT (paste a valid unified diff) OR DIFF_B64 with DIFF_SHA256
   - Optional: FILE_BLOBS for adding new files via base64 (text or binary)
3) Run:
   python pr_from_diff_TEMPLATE.py

Flow:
- clone to /mnt/scratch/…
- create branch from origin/develop
- ensure labels exist (auto-create if missing)
- apply diff (normalized to LF) and/or FILE_BLOBS
- commit, push, open PR against develop

LICENSE
-------
Public domain / CC0. Adapt as needed.
"""

from __future__ import annotations
import base64
import hashlib
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

OWNER = "pvliesdonk"
REPO  = "<REPO_NAME_HERE>"   # TODO: set your repository name (no owner)
BASE_BRANCH = "develop"      # PR base
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

# Provide EITHER a raw diff or a base64-encoded diff with expected sha256.
DIFF_CONTENT = r"""
# --- PASTE YOUR UNIFIED DIFF HERE ---
"""
DIFF_B64 = ""       # base64-encoded unified diff (preferred if content is delicate)
DIFF_SHA256 = ""    # expected sha256 hex digest of the decoded diff payload

# Optional file blobs: repo-relative path -> base64-encoded file content.
FILE_BLOBS: Dict[str, str] = {}

# Labels and reviewers. Missing labels are created automatically.
PR_LABELS = ["from-ai", "needs-review"]
LABEL_COLORS = {
    "from-ai": "5319e7",         # purple
    "needs-review": "d93f0b",    # orange
    "blocked": "b60205",         # red
    "security": "000000",        # black
    "breaking-change": "e11d21", # red
    "docs": "0e8a16",            # green
    "chore": "c5def5",           # light blue
    "content": "1d76db",         # blue
    "design": "fbca04",          # yellow
    "asset": "bfdadc",           # teal
}
PR_REVIEWERS: List[str] = []     # e.g., ["pvliesdonk"]

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
    r = run(["git", "fetch", "--all", "--prune"], cwd=WORKDIR)
    if r.code != 0:
        sys.exit(f"ERROR: git fetch failed\n{r.err or r.out}")

    r = run(["git", "checkout", BASE_BRANCH], cwd=WORKDIR)
    if r.code != 0:
        sys.exit(f"ERROR: base branch '{BASE_BRANCH}' not found locally.\n{r.err or r.out}")

    r = run(["git", "reset", "--hard", f"origin/{BASE_BRANCH}"], cwd=WORKDIR)
    if r.code != 0:
        sys.exit(f"ERROR: failed to reset to origin/{BASE_BRANCH}\n{r.err or r.out}")

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

# ---- Label management ----

def ensure_labels():
    res = run(["gh", "label", "list", "--json", "name"], cwd=WORKDIR)
    existing = set()
    if res.code == 0 and res.out.strip():
        try:
            import json
            data = json.loads(res.out)
            existing = {it["name"] for it in data if "name" in it}
        except Exception:
            existing = {line.split()[0] for line in res.out.splitlines() if line.strip()}
    for name in PR_LABELS:
        if name in existing:
            continue
        color = LABEL_COLORS.get(name, "bfdadc")
        desc = f"Auto-created by PR script — label '{name}'"
        r = run(["gh", "label", "create", name, "--color", color, "--description", desc], cwd=WORKDIR)
        if r.code != 0:
            print(f"WARNING: failed to create label '{name}':\n{r.err or r.out}", file=sys.stderr)

# ---- Diff handling ----

def normalized_diff_bytes() -> bytes:
    if DIFF_B64.strip():
        diff = base64.b64decode(DIFF_B64)
        if DIFF_SHA256:
            import hashlib
            h = hashlib.sha256(diff).hexdigest()
            if h.lower() != DIFF_SHA256.lower():
                sys.exit(f"ERROR: DIFF_SHA256 mismatch: expected {DIFF_SHA256}, got {h}")
        return diff.replace(b"\r\n", b"\n")
    elif DIFF_CONTENT.strip() and not DIFF_CONTENT.strip().startswith("# --- PASTE"):
        return DIFF_CONTENT.replace("\r\n", "\n").encode("utf-8")
    else:
        return b""

def apply_diff_and_blobs():
    diff_bytes = normalized_diff_bytes()
    if diff_bytes:
        diff_file = WORKDIR / "changes.diff"
        diff_file.write_bytes(diff_bytes)
        r = run(["git", "apply", "--index", "--whitespace=fix", str(diff_file)], cwd=WORKDIR)
        if r.code != 0:
            r2 = run(["patch", "-p1", "-N", "-r", "rejections.log", "-i", str(diff_file)], cwd=WORKDIR)
            if r2.code != 0:
                sys.exit("ERROR: failed to apply diff via git apply and patch.\n"
                         f"git apply:\n{r.err or r.out}\npatch:\n{r2.err or r2.out}")
    else:
        if not FILE_BLOBS:
            sys.exit("ERROR: No DIFF provided and FILE_BLOBS is empty. "
                     "Edit this script and provide DIFF_CONTENT or DIFF_B64.")

    for path, b64 in FILE_BLOBS.items():
        target = WORKDIR / path
        target.parent.mkdir(parents=True, exist_ok=True)
        data = base64.b64decode(b64.encode("ascii"))
        target.write_bytes(data)
        r = run(["git", "add", path], cwd=WORKDIR)
        if r.code != 0:
            sys.exit(f"ERROR: git add failed for {path}\n{r.err or r.out}")

def commit_and_push(branch: str):
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
    ensure_labels()
    apply_diff_and_blobs()
    commit_and_push(branch)
    create_pr(branch)
    print(f"SUCCESS: Opened PR from '{branch}' into '{BASE_BRANCH}' for {repo_slug()}")

if __name__ == "__main__":
    main()
