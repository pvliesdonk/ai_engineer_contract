#!/usr/bin/env python3
# Intent: Template script to open a PR using a provided diff or file blobs.
# Auto-detects owner/repo from the current git remote or gh context; CLI/env overrides remain available.
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
from typing import Optional, Tuple

# Contract v2.3.0: base branch is always 'develop' (no env override).
DEFAULT_BASE_BRANCH = "develop"
PR_TITLE = "feat: <edit me>"
PR_BODY = "# Summary\n<why/changes/validation/risk>"
PR_LABELS = ["from-ai", "needs-review"]
LABEL_COLORS = {
    "from-ai": "5319e7",
    "needs-review": "d93f0b",
    "docs": "0e8a16",
    "chore": "c5def5",
    "security": "000000",
    "blocked": "b60205",
    "breaking-change": "e11d21",
    "content": "1d76db",
    "design": "fbca04",
    "asset": "bfdadc",
    "deviation-approved": "5319e7",
}
DIFF_B64 = ""
DIFF_CONTENT = r""
FILE_BLOBS: dict[str, str] = {}
SCRATCH = Path("/mnt/scratch")
TS = datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def run(cmd: list[str], cwd: Optional[str] = None, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        sys.exit(proc.stderr or f"command failed: {' '.join(cmd)}")
    return proc


def parse_slug(url: str) -> Optional[Tuple[str, str]]:
    value = url.strip()
    if not value:
        return None
    if value.endswith(".git"):
        value = value[:-4]
    if value.startswith("git@"):
        _, _, tail = value.partition(":")
        value = tail
    elif "://" in value:
        _, _, tail = value.partition("github.com/")
        value = tail
    if "/" not in value:
        return None
    owner, repo = value.split("/", 1)
    if not owner or not repo:
        return None
    return owner, repo


def detect_repo_slug(cli_owner: Optional[str], cli_repo: Optional[str]) -> Tuple[str, str]:
    if cli_owner and cli_repo:
        return cli_owner, cli_repo

    gh_proc = subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if gh_proc.returncode == 0:
        try:
            data = json.loads(gh_proc.stdout or "{}")
            slug = data.get("nameWithOwner")
            if slug and "/" in slug:
                owner, repo = slug.split("/", 1)
                return owner, repo
        except json.JSONDecodeError:
            pass

    git_proc = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if git_proc.returncode == 0:
        parsed = parse_slug(git_proc.stdout or "")
        if parsed:
            return parsed

    sys.exit("ERROR: unable to determine owner/repo. Pass --owner/--repo or configure git remote/gh.")


def ensure_tools() -> None:
    for tool in ("git", "gh"):
        if run([tool, "--version"], check=False).returncode != 0:
            sys.exit(f"ERROR: {tool} not found")


def normalized_diff() -> bytes:
    data = base64.b64decode(DIFF_B64) if DIFF_B64 else DIFF_CONTENT.encode()
    return data.replace(b"\r\n", b"\n")


def repo_slug(owner: str, repo: str) -> str:
    return f"{owner}/{repo}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", help="Target GitHub owner (auto-detected from gh/git when omitted)")
    parser.add_argument("--repo", help="Target GitHub repository (auto-detected when omitted)")
    parser.add_argument("--base-branch", default=DEFAULT_BASE_BRANCH, help="Base branch for the PR (always 'develop')")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions without cloning/pushing")
    args = parser.parse_args()

    ensure_tools()
    owner, repo = detect_repo_slug(args.owner, args.repo)
    base_branch = args.base_branch
    slug = repo_slug(owner, repo)

    if run(["gh", "repo", "view", slug], check=False).returncode != 0:
        sys.exit("ERROR: cannot view repo (check auth/permissions)")

    if args.dry_run:
        print("DRY-RUN OK", slug, base_branch, PR_TITLE, list(FILE_BLOBS))
        return

    work = SCRATCH / f"pr_{owner}_{repo}_{TS}"
    work.mkdir(parents=True, exist_ok=True)
    if run(["gh", "repo", "clone", slug, str(work)], check=False).returncode != 0:
        sys.exit("clone failed")

    for command in (
        ["git", "fetch", "--all", "--prune"],
        ["git", "checkout", base_branch],
        ["git", "reset", "--hard", f"origin/{base_branch}"],
    ):
        if run(command, cwd=str(work), check=False).returncode != 0:
            sys.exit("git prep failed")

    slugified_title = re.sub(r"[^a-z0-9]+", "-", PR_TITLE.lower()).strip("-") or "changes"
    branch = f"ai/{slugified_title[:40]}-{TS}"
    if run(["git", "switch", "-c", branch], cwd=str(work), check=False).returncode != 0:
        sys.exit("branch create failed")

    existing_labels = set()
    label_list = run(["gh", "label", "list", "--json", "name"], cwd=str(work), check=False)
    if label_list.returncode == 0 and label_list.stdout:
        try:
            existing_labels = {item["name"] for item in json.loads(label_list.stdout)}
        except json.JSONDecodeError:
            existing_labels = set()

    for label in PR_LABELS:
        if label not in existing_labels:
            color = LABEL_COLORS.get(label, "bfdadc")
            run(
                [
                    "gh",
                    "label",
                    "create",
                    label,
                    "--color",
                    color,
                    "--description",
                    f"Auto-created label - {label}",
                ],
                cwd=str(work),
                check=False,
            )

    changed = False
    if DIFF_B64 or DIFF_CONTENT:
        diff_file = work / "changes.diff"
        diff_file.write_bytes(normalized_diff())
        if run(["git", "apply", "--index", "--whitespace=fix", str(diff_file)], cwd=str(work), check=False).returncode != 0:
            sys.exit("apply diff failed")
        changed = True

    for path, b64 in FILE_BLOBS.items():
        target = work / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(base64.b64decode(b64))
        run(["git", "add", path], cwd=str(work))
        changed = True

    if not changed:
        sys.exit("no changes to commit")

    if run(["git", "commit", "-m", PR_TITLE], cwd=str(work), check=False).returncode != 0:
        sys.exit("commit failed")

    if run(["git", "push", "-u", "origin", "HEAD"], cwd=str(work), check=False).returncode != 0:
        sys.exit("push failed")

    pr_cmd = ["gh", "pr", "create", "--title", PR_TITLE, "--body", PR_BODY, "--base", base_branch]
    for label in PR_LABELS:
        pr_cmd += ["--label", label]
    run(pr_cmd, cwd=str(work))

if __name__ == "__main__":
    main()
