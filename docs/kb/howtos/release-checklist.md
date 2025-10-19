---
doc_type: kb_page
doc_version: 2025-10-19.r1
title: Release Checklist
---

# Release Checklist

Use this checklist before promoting a release PR or cutting a tag with release-please.

1. **Validate contract version references**

   ```bash
   python ai/check_version_refs.py
   ```

   Ensure the script exits successfully; fix any drift it reports before continuing.

2. **Review release PR contents**
   - Confirm `CHANGELOG.md` reflects the upcoming tag and lists the correct highlights.
   - Verify documentation updates (contract, capsule, README, KB) match the new version number.

3. **Inspect release notes (dry-run or staged)**
   - Run `gh release view <tag> --json body` after staging to ensure notes mention the latest changes.
   - If release-please is generating notes, skim the PR description to ensure it captures the right commits.

4. **Back-merge and artifacts**
   - After publishing, make sure the automated back-merge from `main` → `develop` completes.
   - Update any outstanding release-trigger docs if manual clean-up was required.

Document deviations or manual fixes in the release PR for traceability.
