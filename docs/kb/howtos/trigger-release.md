---
doc_type: kb_page
doc_version: 2025-01-01.r1
title: Triggering a Release (Repo-specific)
---

# Triggering a Release (Repo-specific)

## Intent

- This repository uses release-please on `main`. For non-feature/non-fix changes (e.g., docs-only), you can force a SemVer bump using a Release-As footer.

## Use the Helper Script

```
python tools/trigger_release.py 2.0.3 --type docs --reason "Publish latest contract clarifications"
```

- Options:
  - `--type feat|fix|docs|chore` (default: docs). Use `feat` to indicate a minor, `fix` for patch behavior in commit semantics.
  - `--breaking` to mark a major release (`!` + BREAKING CHANGE footer in the commit).
  - `--reason` short explanation for the PR and marker file.

The script:
- Creates a branch `release/trigger-<version>` off `origin/main`.
- Adds `docs/release-trigger-<version>.md` as a minimal change.
- Commits with Conventional Commit + `Release-As: <version>` footer.
- Opens a PR to `main` with labels.

## Choosing the Right SemVer for Contract Changes

- Breaking normative change (tightens or changes rules):
  - Commit: `docs(contract)!: ...` and add a `BREAKING CHANGE:` footer; prefer `--breaking` in the helper.
  - Version: MAJOR.
- New normative capability/allowance: `feat(contract): ...`; Version: MINOR.
- Clarification/bug fix in wording without changing behavior: `fix(contract): ...`; Version: PATCH.
- Editorial/formatting only:
  - `docs(contract): ...`; may not create a release automatically. Use the helper to force a patch release when you want a tag.

Reference: `.github/release-please-config.json` and `docs/design/ENGINEERING_CONTRACT.md`.

