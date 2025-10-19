---
doc_type: kb_page
doc_version: 2025-10-19.r2
title: Release Checklist
---

# Release Checklist

Use this checklist before promoting a release PR or cutting a tag with release-please.

1. **Confirm release automation is ready**
   - `RELEASE_PLEASE_TOKEN` should point to a PAT/App token with repo write access (a classic PAT with the `repo` scope works best).
   - The `release-please` workflow runs automatically on pushes to `main`; keep `workflow_dispatch` available for manual retries if needed.

2. **Validate contract version references**

   ```bash
   python ai/check_version_refs.py
   ```

   Ensure the script exits successfully; fix any drift it reports before continuing.

3. **Review release PR contents**
   - Confirm `CHANGELOG.md` reflects the upcoming tag and lists the correct highlights.
   - Verify documentation updates (contract, capsule, README, KB) match the new version number.

4. **Inspect release notes (dry-run or staged)**
   - Run `gh release view <tag> --json body` after staging to ensure notes mention the latest changes.
   - If release-please is generating notes, skim the PR description to ensure it captures the right commits.

5. **Back-merge and artifacts**
   - After publishing, make sure the automated back-merge from `main` → `develop` completes.
   - Update any outstanding release-trigger docs if manual clean-up was required.

Document deviations or manual fixes in the release PR for traceability.
