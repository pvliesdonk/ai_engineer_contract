#!/usr/bin/env python3
# Intent: Template to open a PR that syncs the canonical ENGINEERING_CONTRACT.md
# and optional canonical tools into a target repo (base = develop). Tool-agnostic.
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# Target repo (edit these for your repo when using this template)
OWNER = "pvliesdonk"
REPO = "<REPO_NAME_HERE>"

# Base branch for the target repo (honor env override for portability)
BASE_BRANCH = os.getenv("BASE_BRANCH", "develop")

# Canonical source
SRC_OWNER = "pvliesdonk"
SRC_REPO = "ai_engineer_contract"
SRC_REF = "main"

PR_TITLE = "docs(contract): sync canonical contract/tools"
PR_BODY = (
    "# Summary\n"
    "Sync canonical ENGINEERING_CONTRACT.md and optional canonical tools from"
    f" {SRC_OWNER}/{SRC_REPO}@{SRC_REF} into this repository.\n\n"
    "# Notes\n"
    "- Contract only by default; pass --include-tools to also update *TEMPLATE* tools.\n"
    "- Avoids overwriting non-template local tools.\n"
)

SCRATCH = Path("/mnt/scratch")
TS = datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def run(cmd: list[str], cwd: str | None = None, check: bool = True) -> subprocess.CompletedProcess:
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        sys.exit(p.stderr or f"command failed: {' '.join(cmd)}")
    return p


def gh_api(path: str) -> dict | list:
    r = run(["gh", "api", path], check=True)
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit(f"ERROR: failed to parse gh api output for {path}")


def b64_to_bytes(content_b64: str) -> bytes:
    return base64.b64decode(content_b64.encode("utf-8"))


def fetch_content(owner: str, repo: str, path: str, ref: str) -> bytes:
    data = gh_api(f"repos/{owner}/{repo}/contents/{path}?ref={ref}")
    if isinstance(data, dict) and data.get("content"):
        return b64_to_bytes(data["content"])
    sys.exit(f"ERROR: cannot fetch {owner}/{repo}:{path}@{ref}")


def list_dir(owner: str, repo: str, path: str, ref: str) -> list[dict]:
    data = gh_api(f"repos/{owner}/{repo}/contents/{path}?ref={ref}")
    if isinstance(data, list):
        return data
    sys.exit(f"ERROR: cannot list {owner}/{repo}:{path}@{ref}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Sync canonical contract and optional tools")
    ap.add_argument("--owner", default=OWNER, help="Target owner")
    ap.add_argument("--repo", default=REPO, help="Target repo")
    ap.add_argument("--include-tools", action="store_true", help="Also sync canonical *TEMPLATE* tools")
    ap.add_argument("--dry-run", action="store_true", help="Do not push/PR; print planned changes")
    a = ap.parse_args()

    # Tool checks
    for t in ("git", "gh"):
        if run([t, "--version"], check=False).returncode != 0:
            sys.exit(f"ERROR: {t} not found")

    # Prepare workspace
    work = SCRATCH / f"sync_{a.owner}_{a.repo}_{TS}"
    work.mkdir(parents=True, exist_ok=True)
    if run(["gh", "repo", "clone", f"{a.owner}/{a.repo}", str(work)], check=False).returncode != 0:
        sys.exit("ERROR: clone failed (check repo permissions)")
    for c in (["git", "fetch", "--all", "--prune"], ["git", "checkout", BASE_BRANCH], ["git", "reset", "--hard", f"origin/{BASE_BRANCH}"]):
        if run(c, cwd=str(work), check=False).returncode != 0:
            sys.exit("ERROR: git prep failed")

    # Create branch
    branch = f"docs/sync-contract-{TS}"
    if run(["git", "switch", "-c", branch], cwd=str(work), check=False).returncode != 0:
        sys.exit("ERROR: branch create failed")

    changed = False
    planned: list[str] = []

    # Sync contract
    target_contract = work / "docs" / "design" / "ENGINEERING_CONTRACT.md"
    target_contract.parent.mkdir(parents=True, exist_ok=True)
    new_contract = fetch_content(SRC_OWNER, SRC_REPO, "docs/design/ENGINEERING_CONTRACT.md", SRC_REF)
    old_contract = target_contract.read_bytes() if target_contract.exists() else b""
    if new_contract != old_contract:
        target_contract.write_bytes(new_contract)
        run(["git", "add", str(target_contract.relative_to(work))], cwd=str(work))
        changed = True
        planned.append("ENGINEERING_CONTRACT.md")

    # Optionally sync canonical tool templates (*_TEMPLATE.py only)
    if a.include_tools:
        entries = list_dir(SRC_OWNER, SRC_REPO, "tools", SRC_REF)
        for entry in entries:
            name = entry.get("name", "")
            if not name.endswith("_TEMPLATE.py"):
                continue  # avoid overwriting local non-template tools
            content = fetch_content(SRC_OWNER, SRC_REPO, f"tools/{name}", SRC_REF)
            dest = work / "tools" / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            old = dest.read_bytes() if dest.exists() else b""
            if content != old:
                dest.write_bytes(content)
                run(["git", "add", str(dest.relative_to(work))], cwd=str(work))
                changed = True
                planned.append(f"tools/{name}")

    if a.dry_run:
        print("DRY RUN")
        print("Base branch:", BASE_BRANCH)
        print("Planned changes:")
        for p in planned:
            print("-", p)
        return

    if not changed:
        sys.exit("no changes to sync")

    # Commit and PR
    if run(["git", "commit", "-m", PR_TITLE], cwd=str(work), check=False).returncode != 0:
        sys.exit("ERROR: commit failed")
    if run(["git", "push", "-u", "origin", branch], cwd=str(work), check=False).returncode != 0:
        sys.exit("ERROR: push failed")

    # Ensure labels exist
    for name, color in {
        "from-ai": "5319e7",
        "needs-review": "d93f0b",
        "docs": "0e8a16",
    }.items():
        run(["gh", "label", "create", name, "--color", color, "--description", f"Auto-created label - {name}", "--force"], cwd=str(work), check=False)

    args = [
        "gh",
        "pr",
        "create",
        "--base",
        BASE_BRANCH,
        "--head",
        branch,
        "--title",
        PR_TITLE,
        "--body",
        PR_BODY,
    ]
    r = run(args, cwd=str(work), check=False)
    if r.returncode != 0:
        sys.exit("ERROR: pr create failed")
    pr_url = r.stdout.strip()
    # Label PR
    run(["gh", "pr", "edit", pr_url, "--add-label", "from-ai", "--add-label", "needs-review", "--add-label", "docs"], cwd=str(work), check=False)
    print(pr_url)


if __name__ == "__main__":
    main()
