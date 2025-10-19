#!/usr/bin/env python3
"""Verify that published version references stay in sync with the capsule version.

Run manually (``python ai/check_version_refs.py``) or wire into CI before cutting a release.
The script treats ``ai/manifest.json::capsuleVersion`` as the source of truth.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, Iterable, List


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "ai" / "manifest.json"


def load_version() -> str:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    version = data.get("capsuleVersion")
    if not version or not isinstance(version, str):
        raise ValueError("capsuleVersion missing from ai/manifest.json")
    if not version.startswith("v"):
        raise ValueError(f"capsuleVersion must start with 'v': {version!r}")
    return version


def first_changelog_version(changelog: str) -> str | None:
    for line in changelog.splitlines():
        line = line.strip()
        if line.startswith("## [") and "]" in line:
            return line[4 : line.index("]")]
    return None


def check_strings(content: str, expectations: Iterable[str], path: Path, errors: List[str]) -> None:
    for expected in expectations:
        if expected not in content:
            errors.append(f"{path.relative_to(REPO_ROOT)} missing '{expected}'")


def main() -> int:
    version = load_version()  # e.g. v2.1.1
    version_plain = version.lstrip("v")

    expectations: Dict[Path, List[str]] = {
        REPO_ROOT / "README.md": [
            f"Contract Capsule {version}",
            f"ACK CONTRACT {version}",
            f"ENGINEERING_CONTRACT.md (v{version_plain})",
        ],
        REPO_ROOT / "ai" / "contract_capsule.md": [
            f"Contract Capsule {version}",
            f"ENGINEERING_CONTRACT.md` (v{version_plain})",
            f"ACK CONTRACT {version}",
        ],
        REPO_ROOT / "ai" / "manifest.json": [f'"capsuleVersion": "{version}"'],
        REPO_ROOT / "CONTRACT_REFERENCE_TEMPLATE.md": [
            f"--source-ref ai_engineer_contract-{version}"
        ],
        REPO_ROOT / "docs" / "kb" / "howtos" / "sync-canonical.md": [
            f"--source-ref ai_engineer_contract-{version}"
        ],
        REPO_ROOT / "docs" / "design" / "ENGINEERING_CONTRACT.md": [
            f"— v{version_plain}",
            f"- v{version_plain} —",
        ],
    }

    errors: List[str] = []

    for path, snippets in expectations.items():
        content = path.read_text(encoding="utf-8")
        check_strings(content, snippets, path, errors)

    changelog_text = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    changelog_version = first_changelog_version(changelog_text)
    if changelog_version != version_plain:
        errors.append(
            f"CHANGELOG.md leading entry is '{changelog_version}' but expected '{version_plain}'"
        )

    if errors:
        print("Version reference check failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"All version references match {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
