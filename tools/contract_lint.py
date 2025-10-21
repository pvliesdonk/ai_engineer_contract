#!/usr/bin/env python3
"""Lightweight contract linting for CI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "ai" / "manifest.json"
LABELS_DOC = ROOT / "docs" / "kb" / "labels.md"

REQUIRED_FILES = [
    "ai/contract_capsule.md",
    "ai/manifest.json",
    "docs/design/ENGINEERING_CONTRACT.md",
    "docs/design/delivery-map.yml",
    "docs/kb/howtos/scm-c-advise.md",
]

REQUIRED_POLICY_KEYS = {
    "base_branch",
    "contract_version",
    "docs",
    "releases",
    "phase_gate",
}

REQUIRED_PHASES = {"requirements", "design", "plan", "build"}


def ensure(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []

    for rel_path in REQUIRED_FILES:
        path = ROOT / rel_path
        ensure(path.exists(), f"Required file missing: {rel_path}", errors)

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append("Manifest ai/manifest.json not found")
        manifest = {}
    except json.JSONDecodeError as exc:
        errors.append(f"Manifest ai/manifest.json is invalid JSON: {exc}")
        manifest = {}

    policy = manifest.get("policy") if isinstance(manifest, dict) else None
    ensure(isinstance(policy, dict), "Manifest policy block missing (ai/manifest.json::policy)", errors)

    if isinstance(policy, dict):
        missing_keys = REQUIRED_POLICY_KEYS - policy.keys()
        ensure(not missing_keys, f"Manifest policy missing keys: {', '.join(sorted(missing_keys))}", errors)

        phase_gate = policy.get("phase_gate") if isinstance(policy.get("phase_gate"), dict) else {}
        if not isinstance(phase_gate, dict):
            errors.append("Manifest policy.phase_gate must be an object")
        else:
            allowed = phase_gate.get("allowed_by_phase") if isinstance(phase_gate.get("allowed_by_phase"), dict) else {}
            missing_phases = REQUIRED_PHASES - set(allowed.keys())
            ensure(not missing_phases, f"allowed_by_phase missing entries for: {', '.join(sorted(missing_phases))}", errors)
            override = phase_gate.get("override_labels") if isinstance(phase_gate.get("override_labels"), dict) else {}
            ensure("plan_exempt" in override, "override_labels.plan_exempt not configured", errors)
            ensure("deviation" in override, "override_labels.deviation not configured", errors)
            ensure("require_plan_ref_in_build" in phase_gate, "phase_gate.require_plan_ref_in_build not configured", errors)

    # Regenerate labels doc and ensure it is clean.
    try:
        subprocess.run([sys.executable, "tools/gen_labels_md.py"], cwd=ROOT, check=True)
    except subprocess.CalledProcessError as exc:
        errors.append(f"Failed to regenerate labels doc: {exc}")
    else:
        diff = subprocess.run(["git", "diff", "--name-only", "--", str(LABELS_DOC.relative_to(ROOT))],
                               cwd=ROOT,
                               capture_output=True,
                               text=True,
                               check=False)
        if diff.stdout.strip():
            errors.append("docs/kb/labels.md is stale; run `python tools/gen_labels_md.py`.\n" + diff.stdout.strip())

    if errors:
        print("Contract lint detected issues:\n", file=sys.stderr)
        for problem in errors:
            print(f"- {problem}", file=sys.stderr)
        return 1

    print("Contract lint passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
