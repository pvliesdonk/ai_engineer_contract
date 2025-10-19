#!/usr/bin/env python3
# Intent: Template script to bootstrap a repository (create via gh, set up develop, labels).
# Auto-detects owner from the authenticated GitHub user; override via CLI flags.
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

LABELS = {
    "from-ai": "5319e7",
    "needs-review": "d93f0b",
    "docs": "0e8a16",
    "chore": "c5def5",
    "security": "000000",
    "blocked": "b60205",
    "planning": "0052cc",
    "needs-design-ref": "1d76db",
    "breaking-change": "e11d21",
    "content": "1d76db",
    "design": "fbca04",
    "asset": "bfdadc",
    "deviation-approved": "5319e7",
}


def run(cmd: list[str], cwd: str | None = None) -> str:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        sys.exit(proc.stderr or f"command failed: {' '.join(cmd)}")
    return proc.stdout


def detect_owner(cli_owner: str | None) -> str:
    if cli_owner:
        return cli_owner
    proc = subprocess.run(
        ["gh", "api", "user", "--jq", ".login"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode == 0 and proc.stdout.strip():
        return proc.stdout.strip()
    sys.exit("ERROR: unable to detect GitHub owner. Pass --owner or ensure gh auth works.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap a repository with develop branch and labels.")
    parser.add_argument("--repo", required=True, help="Repository name to create (slug)")
    parser.add_argument(
        "--owner",
        help="GitHub owner/organisation (defaults to the authenticated gh user)",
    )
    parser.add_argument(
        "--visibility",
        choices=("public", "private", "internal"),
        default=os.getenv("GH_REPO_VISIBILITY", "public"),
        help="Repository visibility passed to gh repo create",
    )
    parser.add_argument("--license", default="MIT", help="Initial licence identifier to include in README header")
    args = parser.parse_args()

    owner = detect_owner(args.owner)
    slug = f"{owner}/{args.repo}"
    visibility_flag = f"--{args.visibility}"

    run(["gh", "repo", "create", slug, visibility_flag, "--confirm"])
    run(["gh", "repo", "clone", slug, args.repo])
    repo = Path(args.repo)

    (repo / ".gitignore").write_text(".venv/\n.DS_Store\n__pycache__/\n", encoding="utf-8")
    (repo / "README.md").write_text(f"# {args.repo}\n\nLicensed under {args.license}.\n", encoding="utf-8")
    (repo / "CONTRIBUTING.md").write_text("# Contributing\n\nDescribe contribution workflow here.\n", encoding="utf-8")

    run(["git", "checkout", "-b", "develop"], cwd=str(repo))
    run(["git", "commit", "--allow-empty", "-m", "chore: initialize develop"], cwd=str(repo))
    run(["git", "push", "-u", "origin", "develop"], cwd=str(repo))

    for name, color in LABELS.items():
        subprocess.run(
            [
                "gh",
                "label",
                "create",
                name,
                "--color",
                color,
                "--description",
                f"Auto-created label - {name}",
            ],
            cwd=str(repo),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    print(f"Repo bootstrap complete for {slug}")


if __name__ == "__main__":
    main()
