---
doc_type: kb_page
doc_version: 2025-10-19.r1
title: Plan → Build Workflow
---

# Plan → Build Workflow

Follow this flow whenever you move from design into implementation.

## 1. Draft the Plan Issue

- Open a new issue using the **Plan** template (`gh issue create --template plan` works too).
- Capture context links (design docs/ADRs), acceptance criteria, validation strategy, and risks.
- Add the issue to the relevant Project column (e.g., _Ready for Build_) so we can track progress.

## 2. Validate & Align

- Share the issue for review. Adjust acceptance criteria or scope until everyone agrees the plan is ready.
- If the plan changes later, update the issue first and call out changes in a comment.

## 3. Reference the Plan from PRs

- Implementation PRs must reference the plan (`Fixes #123` / `Refs #123`) in the body.
- The phase-gate workflow checks for these references when `phase: build`. Without them, the PR fails unless it is explicitly labeled `plan-exempt`.
- Keep the plan issue updated as work lands (status notes, checklists, links to PRs).

## 4. Exceptions

- Reserve the `plan-exempt` label for consciously approved micro-fixes. Document the rationale in both the PR and (if applicable) the related issue.
- Docs-only improvements that happen after the build phase still require a plan reference—documentation is part of the product surface.

## 5. Checklist

Every pre-build PR should confirm:

- [ ] Only planning/doc/ops files changed.
- [ ] Plan issue recorded or updated with acceptance criteria & validation.
- [ ] Requirements/design docs stay in sync with the latest decisions.
