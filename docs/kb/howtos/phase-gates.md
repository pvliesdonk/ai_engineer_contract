---
doc_type: kb_page
doc_version: 2025-10-20.r2
title: Phase Gates — Advance and Troubleshoot
---

# Phase Gates — Advance and Troubleshoot

## Overview

- The repository enforces contract phases via `phase.yaml` and a CI workflow (`.github/workflows/phase-gate.yml`).
- During `pull_request`, CI fails when changes touch paths outside the allowlist for the current phase.

## Phases and Defaults

- requirements/design: allow `docs/**`, `AGENTS.md`, `ai/**`, `phase.yaml`.
- plan: allow the above + `.github/**`.
- build: unrestricted.

You may override defaults by listing `allowed_paths` in `phase.yaml`.

## Advance the Phase

1) Edit `phase.yaml` and set `phase: plan` (or `build`).
2) Commit in a small PR; once merged, subsequent PRs follow the new allowlist.

## Temporary Deviation

- Add label `deviation-approved` to the PR and include a rationale in the PR body.
- CI will accept the deviation, but reviewers should ensure rollback/mitigation.

## Quick-Escape (when CI blocks your PR)

1) Add a **Plan issue link** (e.g., `Fixes #123`) to the PR body to satisfy the plan-before-build gate.
2) For **micro-fixes**, apply the `plan-exempt` label and explain the rationale.
3) If urgent but non-conforming, request a maintainer to apply `deviation-approved` and capture the rationale in the PR.

## Troubleshooting

- CI shows “Disallowed changes…”: review the listed files and adjust `phase.yaml` or split the PR.
- Ensure the PR runs against `develop` and that `phase.yaml` is present at the repo root.
- For nested workflows or non-standard paths, add them to `allowed_paths`.
