---
doc_type: kb_howto
doc_version: 2025-10-20.r1
title: Advise-Only Mode (formerly SCM-C) — Templates
---

# Advise-Only Mode (formerly SCM-C)

Advise-only mode means you **do not** change the repo state directly. You deliver changes as issues, PR bodies, review comments, or single-file diffs. Humans apply them.

Use these templates verbatim and adapt the checklists to the repo’s quality bar.

## Issue Template — Plan Before Build

````md
**Summary**
<one line>

**Context & Links**
- Refs #<umbrella>

**Acceptance Criteria**
- [ ] <measurable outcome>

**Validation**
- <command(s) to run>

**Phase**
plan (docs/ops-only)
````

## PR Body Template — Docs/Config Only

````md
# Summary

# Why

# Changes

# Validation

> Quick reference: **Phase Gate Quick-Escape** — see `docs/kb/howtos/phase-gates.md`.

## Linked Issues
- Fixes #<id>
- Refs #<id>
````

## Review Comment — Single-File Diff

````diff
*** path/to/file.ext
@@
- old line
+ new line
````

## Deviation Request (when gates block work)

> Label: `deviation-approved` (maintainer applies)

- Rationale: <why risk is acceptable>
- Mitigation: <rollback or follow-up>
- Scope: <files/paths>
