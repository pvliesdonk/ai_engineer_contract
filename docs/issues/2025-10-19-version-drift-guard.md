# Issue: Guard against version-reference drift

## Problem
- Each release bumps the contract/capsule version (now `v2.1.1`), but multiple docs embed the previous value.
- Manual updates are error-prone; the latest release shipped before those references were refreshed.

## Proposal
- Pick a single source of truth (e.g., `ai/manifest.json::capsuleVersion`).
- Add a lightweight checker that asserts all known references (`README.md`, `docs/design/ENGINEERING_CONTRACT.md`, `ai/contract_capsule.md`, `CONTRACT_REFERENCE_TEMPLATE.md`, `docs/kb/howtos/sync-canonical.md`, CHANGELOG header, etc.) match that value.
- Run the checker in CI (and locally via `make test`/`nox`/`tox` equivalent) so releases fail fast when the versions drift.

## Acceptance Criteria
- CI fails when any tracked file contains a version that diverges from the canonical value.
- The checker is easy to run locally and documented for release managers.
- Release checklist references the checker so future bumps include it.

## Status
- [x] Added `ai/check_version_refs.py` to validate references locally.
- [x] Wired the checker into the `python-scripts-smoke` workflow.
- [x] Documented the checklist in `docs/kb/howtos/release-checklist.md`.

## Notes
- Optionally expose the checker as `python ai/check_version_refs.py` or similar so it fits within the current allowed paths.
- Consider extending release automation to rewrite the files automatically, but the immediate goal is detection.
