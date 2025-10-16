#!/usr/bin/env python3
# Intent: Repo-specific helper to open a PR against 'main' that forces a
# release via release-please using a Release-As footer. It creates a small
# marker file and opens a PR with the right commit message and labels.
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: str | None = None, check: bool = True) -> subprocess.CompletedProcess:
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        sys.exit(p.stderr or f"command failed: {' '.join(cmd)}")
    return p


def main() -> None:
    ap = argparse.ArgumentParser(description="Trigger a release via Release-As in a PR to main")
    ap.add_argument("version", help="SemVer to release, e.g. 2.0.3")
    ap.add_argument("--type", default="docs", choices=["feat", "fix", "docs", "chore"], help="Conventional type")
    ap.add_argument("--breaking", action="store_true", help="Mark as breaking change (! and BREAKING CHANGE footer)")
    ap.add_argument("--reason", default="Align documentation and configuration for release", help="Short reason")
    ap.add_argument("--no-open", action="store_true", help="Do not open PR; just prepare commit locally")
    args = ap.parse_args()

    version = args.version.strip().lstrip("v")
    branch = f"release/trigger-{version}"

    # Ensure we are clean and can base on main
    run(["git", "fetch", "origin", "main"], check=True)
    run(["git", "checkout", "-B", branch, "origin/main"], check=True)

    # Create a tiny marker file for traceability
    marker = Path("docs") / f"release-trigger-{version}.md"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"Trigger release {version}: {args.reason}.\n", encoding="utf-8")

    # Compose commit message
    bang = "!" if args.breaking else ""
    subject = f"{args.type}{bang}: trigger release {version}"
    body_lines = [args.reason, "", f"Release-As: {version}"]
    if args.breaking:
        body_lines.append("")
        body_lines.append("BREAKING CHANGE: Contract change considered breaking.")
    body = "\n".join(body_lines)

    run(["git", "add", str(marker)])
    run(["git", "commit", "-m", subject, "-m", body])
    run(["git", "push", "-u", "origin", branch])

    if not args.no_open:
        # Ensure labels exist (idempotent)
        for name, color in {
            "from-ai": "5319e7",
            "docs": "0e8a16",
            "chore": "c5def5",
            "needs-review": "d93f0b",
        }.items():
            subprocess.run(["gh", "label", "create", name, "--color", color, "--description", f"Auto-created label - {name}", "--force"], text=True)

        # Open PR to main
        pr = run([
            "gh", "pr", "create",
            "--base", "main",
            "--head", branch,
            "--title", subject,
            "--body", f"Force a release {version} via Release-As. {args.reason}",
        ])
        url = pr.stdout.strip()
        print(url)
        # Label PR
        run(["gh", "pr", "edit", url, "--add-label", "from-ai", "--add-label", args.type, "--add-label", "needs-review"])


if __name__ == "__main__":
    main()

