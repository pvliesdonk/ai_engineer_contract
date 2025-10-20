#!/usr/bin/env python3
# Intent: Template to open a PR that syncs the canonical ENGINEERING_CONTRACT.md
# and optional canonical tools into a target repo (base = develop). Tool-agnostic.
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


def manifest_base_branch() -> str:
    manifest = Path("ai/manifest.json")
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            branch = data.get("baseBranch")
            if branch:
                return branch
        except json.JSONDecodeError:
            pass
    return "develop"


DEFAULT_BASE_BRANCH = "develop"  # contract v2.2.0

# Canonical source (defaults; may be overridden by ai/sync.config.json or CLI)
SRC_OWNER = "pvliesdonk"
SRC_REPO = "ai_engineer_contract"
SRC_REF = "latest"  # "latest" uses latest GitHub release tag, else a ref like "main" or a tag/sha

PR_TITLE = "docs(contract): sync canonical (from {ref})"
PR_BODY_TMPL = (
    "# Summary\n"
    "Sync canonical ENGINEERING_CONTRACT.md and optional canonical tools from {src_owner}/{src_repo}@{ref}.\n\n"
    "# Notes\n"
    "- Contract only by default; pass --include-tools to also update *TEMPLATE* tools.\n"
    "- Avoids overwriting non-template local tools.\n"
)

SCRATCH = Path("/mnt/scratch")
TS = datetime.utcnow().strftime("%Y%m%d_%H%M%S")


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


def detect_target_slug(cli_owner: Optional[str], cli_repo: Optional[str]) -> Tuple[str, str]:
    if cli_owner and cli_repo:
        return cli_owner, cli_repo

    gh_proc = subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if gh_proc.returncode == 0 and gh_proc.stdout:
        try:
            data = json.loads(gh_proc.stdout)
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

    sys.exit("ERROR: unable to determine target owner/repo. Provide --owner/--repo or configure git/gh.")


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


def latest_release_tag(owner: str, repo: str) -> str:
    try:
        data = gh_api(f"repos/{owner}/{repo}/releases/latest")
        return data.get("tag_name")
    except SystemExit:
        # Fallback: latest tag
        tags = gh_api(f"repos/{owner}/{repo}/tags")
        if isinstance(tags, list) and tags:
            return tags[0].get("name")
        sys.exit("ERROR: cannot resolve latest release/tag")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_synced_sha(text: str) -> str | None:
    # Look for markers like: <!-- synced_from: owner/repo@ref sha=abcdef -->
    m = re.search(r"synced_from: .*? sha=([0-9a-f]{8,64})", text)
    return m.group(1) if m else None


def main() -> None:
    ap = argparse.ArgumentParser(description="Sync canonical contract and optional tools")
    ap.add_argument("--owner", help="Target owner (auto-detected from gh/git when omitted)")
    ap.add_argument("--repo", help="Target repo (auto-detected when omitted)")
    ap.add_argument("--base-branch", default=DEFAULT_BASE_BRANCH, help="Base branch for the target repo (default: %(default)s)")
    ap.add_argument("--include-tools", action="store_true", help="Also sync canonical *TEMPLATE* tools")
    ap.add_argument("--include-capsule", action="store_true", help="Also sync ai/contract_capsule.md")
    ap.add_argument("--source-ref", default=None, help="Override source ref (tag/sha/branch). Default comes from config or 'latest'")
    ap.add_argument("--force", action="store_true", help="Overwrite even if target shows a different synced sha")
    ap.add_argument("--dry-run", action="store_true", help="Do not push/PR; print planned changes")
    a = ap.parse_args()

    # Tool checks
    for t in ("git", "gh"):
        if run([t, "--version"], check=False).returncode != 0:
            sys.exit(f"ERROR: {t} not found")

    owner, repo = detect_target_slug(a.owner, a.repo)
    base_branch = a.base_branch

    # Load config if present
    cfg_path = Path("ai/sync.config.json")
    cfg = {}
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception:
            cfg = {}

    src_owner = (cfg.get("sourceRepo") or f"{SRC_OWNER}/{SRC_REPO}")
    if "/" in src_owner:
        c_owner, c_repo = src_owner.split("/", 1)
    else:
        c_owner, c_repo = SRC_OWNER, SRC_REPO
    ref_cfg = cfg.get("sourceRef", SRC_REF)
    ref = a.source_ref or ref_cfg
    if ref == "latest":
        ref = latest_release_tag(c_owner, c_repo)

    sync_contract = bool(cfg.get("syncContract", True))
    sync_tools_patterns = cfg.get("syncTools", ["*_TEMPLATE.py"])
    include_capsule = a.include_capsule or bool(cfg.get("includeCapsule", False))

    # Prepare workspace
    work = SCRATCH / f"sync_{owner}_{repo}_{TS}"
    work.mkdir(parents=True, exist_ok=True)
    if run(["gh", "repo", "clone", f"{owner}/{repo}", str(work)], check=False).returncode != 0:
        sys.exit("ERROR: clone failed (check repo permissions)")
    for c in (["git", "fetch", "--all", "--prune"], ["git", "checkout", base_branch], ["git", "reset", "--hard", f"origin/{base_branch}"]):
        if run(c, cwd=str(work), check=False).returncode != 0:
            sys.exit("ERROR: git prep failed")

    # Create branch
    branch = f"docs/sync-contract-{TS}"
    if run(["git", "switch", "-c", branch], cwd=str(work), check=False).returncode != 0:
        sys.exit("ERROR: branch create failed")

    changed = False
    planned: list[tuple[str, str, int]] = []  # path, sha, size

    # Sync contract
    if sync_contract:
        target_contract = work / "docs" / "design" / "ENGINEERING_CONTRACT.md"
        target_contract.parent.mkdir(parents=True, exist_ok=True)
        content = fetch_content(c_owner, c_repo, "docs/design/ENGINEERING_CONTRACT.md", ref)
        src_sha = sha256(content)[:12]
        footer = f"\n\n<!-- synced_from: {c_owner}/{c_repo}@{ref} sha={src_sha} ts={TS} -->\n"
        new_contract = content + footer.encode("utf-8")
        old_contract = target_contract.read_bytes() if target_contract.exists() else b""
        if new_contract != old_contract:
            # Overwrite safety if old has a different synced sha
            if old_contract:
                old_sha = parse_synced_sha(old_contract.decode("utf-8", errors="ignore"))
                if old_sha and old_sha != src_sha and not a.force:
                    sys.exit("refusing to overwrite contract with different synced sha; use --force to proceed")
            target_contract.write_bytes(new_contract)
            run(["git", "add", str(target_contract.relative_to(work))], cwd=str(work))
            changed = True
            planned.append(("docs/design/ENGINEERING_CONTRACT.md", src_sha, len(new_contract)))

    # Optionally sync canonical tool templates (*_TEMPLATE.py only)
    if a.include_tools and sync_tools_patterns:
        entries = list_dir(c_owner, c_repo, "tools", ref)
        for entry in entries:
            name = entry.get("name", "")
            if not any(re.fullmatch(p.replace("*", ".*"), name) for p in sync_tools_patterns):
                continue  # avoid overwriting local non-template tools
            content = fetch_content(c_owner, c_repo, f"tools/{name}", ref)
            src_sha = sha256(content)[:12]
            header = (
                f"# Synced from {c_owner}/{c_repo}@{ref} sha={src_sha} ts={TS}\n"
                f"# Do not edit directly if you plan to re-sync; local changes may be overwritten.\n"
            ).encode("utf-8")
            if content.startswith(b"#!/"):
                # preserve shebang on first line
                first, rest = content.split(b"\n", 1)
                body = first + b"\n" + header + rest
            else:
                body = header + content
            dest = work / "tools" / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            old = dest.read_bytes() if dest.exists() else b""
            if body != old:
                if old:
                    old_sha = parse_synced_sha(old.decode("utf-8", errors="ignore"))
                    if old_sha and old_sha != src_sha and not a.force:
                        sys.exit(f"refusing to overwrite {name} with different synced sha; use --force to proceed")
                dest.write_bytes(body)
                run(["git", "add", str(dest.relative_to(work))], cwd=str(work))
                changed = True
                planned.append((f"tools/{name}", src_sha, len(body)))

    # Optionally sync capsule
    if include_capsule:
        cap_src = fetch_content(c_owner, c_repo, "ai/contract_capsule.md", ref)
        cap_sha = sha256(cap_src)[:12]
        footer = f"\n\n<!-- synced_from: {c_owner}/{c_repo}@{ref} sha={cap_sha} ts={TS} -->\n"
        cap_new = cap_src + footer.encode("utf-8")
        cap_tgt = work / "ai" / "contract_capsule.md"
        cap_tgt.parent.mkdir(parents=True, exist_ok=True)
        cap_old = cap_tgt.read_bytes() if cap_tgt.exists() else b""
        if cap_new != cap_old:
            if cap_old:
                old_sha = parse_synced_sha(cap_old.decode("utf-8", errors="ignore"))
                if old_sha and old_sha != cap_sha and not a.force:
                    sys.exit("refusing to overwrite capsule with different synced sha; use --force to proceed")
            cap_tgt.write_bytes(cap_new)
            run(["git", "add", str(cap_tgt.relative_to(work))], cwd=str(work))
            changed = True
            planned.append(("ai/contract_capsule.md", cap_sha, len(cap_new)))

    if a.dry_run:
        print("DRY RUN")
        print("Target:", f"{owner}/{repo}")
        print("Base branch:", base_branch)
        print("Source:", f"{c_owner}/{c_repo}@{ref}")
        if not planned:
            print("No changes.")
            return
        print("Planned changes:")
        for path, sha, size in planned:
            print(f"- {path} (sha={sha}, size={size} bytes)")
        return

    if not changed:
        sys.exit("no changes to sync")

    # Commit and PR
    commit_title = PR_TITLE.format(ref=ref)
    if run(["git", "commit", "-m", commit_title], cwd=str(work), check=False).returncode != 0:
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

    body = PR_BODY_TMPL.format(src_owner=c_owner, src_repo=c_repo, ref=ref)
    args = [
        "gh",
        "pr",
        "create",
        "--base",
        base_branch,
        "--head",
        branch,
        "--title",
        commit_title,
        "--body",
        body,
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
