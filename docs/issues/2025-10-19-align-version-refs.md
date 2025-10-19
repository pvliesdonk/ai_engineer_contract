# Issue: Align version references with v2.1.1

## Summary
- Tag `ai_engineer_contract-v2.1.1` exists, but docs still mention the old capsule `v2.0.2` and changelog tops out at `v2.1.0`.
- Readers and tooling following the documented version drift behind what the release actually ships.

## Scope
- Update `CHANGELOG.md` so the latest entry reflects `v2.1.1` with a brief, correct summary.
- Bump hard-coded capsule/version references in:
  - `README.md`
  - `ai/contract_capsule.md`
  - `ai/manifest.json`
  - `docs/design/ENGINEERING_CONTRACT.md`
  - `docs/kb/howtos/sync-canonical.md`
  - `CONTRACT_REFERENCE_TEMPLATE.md`
- Check for any other lingering `v2.0.2` mentions and refresh them to `v2.1.1`.

## Acceptance Criteria
- All public docs and helper scripts point at `v2.1.1`.
- CHANGELOG documents `v2.1.1` as the latest release.
- Release follow-ups (e.g., `release-trigger-*` docs) capture any automation or manual steps required.

## Status
- [x] Updated README, capsule, manifest, contract, and sync docs to `v2.1.1`.
- [x] Added `2.1.1` entry to `CHANGELOG.md`.
- [x] Confirmed release artifacts (`release-please` notes) match the refreshed texts.

## Follow-up
- Coordinate with release automation so the next release automatically aligns these references (see companion prevention issue).
