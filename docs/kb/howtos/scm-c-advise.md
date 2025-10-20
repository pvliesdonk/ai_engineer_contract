---
doc_type: kb_page
doc_version: 2025-10-21.r1
title: SCM-C Advise-Only Templates
---

# SCM-C Advise-Only Templates

## Intent

- Provide ready-to-paste structures for SCM-C (advise-only) sessions.
- Clarify allowed outputs, forbidden actions, and when to escalate to SCM-B/A.
- Keep hand-offs auditable and easy for humans to apply manually.

## Allowed Outputs

- Issue, plan, or PR bodies that follow the contract sections (`Summary`, `Context`, `Acceptance`, etc.).
- Review-ready comment packages: findings list, risk callouts, approval/blocking recommendation.
- Validation and risk checklists that the human can copy into issues/PRs.
- Single-file inline unified diffs contained in fenced code blocks, paired with application notes.

## Forbidden Actions

- No filesystem edits, git commands, or script execution.
- Do not attach archives, binary artifacts, or multi-file patches.
- Avoid automation that would create branches, PRs, labels, or project items directly.

## Escalate When

- The request involves more than one file or requires command/script execution.
- The human wants push-ready patches, CLI automation, or CI runs.
- Security-sensitive work (secrets, repo settings) needs verification in SCM-A.

## Recommended Labeling & Tracking

- Tag issues consuming SCM-C outputs with a local `advise-only` or `planning` label to support reporting.
- Capture lead time from “Proposed solution” comment to merged PR in project dashboards for success metrics.
- Note in the issue/PR comment when handing off that the work followed SCM-C templates.

## Templates

### Issue / Plan Body

```markdown
## Summary
<one sentence outcome>

## Context & Links
- docs/design/<doc>.md
- Related issue #

## Acceptance Criteria
- [ ] <observable result>
- [ ] <observable result>

## Validation
- `command` (expected to be run by human)
- Manual: <steps>

## Risks & Mitigations
- Risk: <risk> — Mitigation: <plan>
```

### Review Comment Package

```markdown
**Findings**
- [ ] Blocking – <description> (`path/to/file.ext:123`)
- [ ] Non-blocking – <description>

**Risks / Follow-up**
- Risk: <explanation>
- Mitigation: <proposal or link>

**Recommendation**
- Approve once blockers resolve.
```

### Status Checklist

```markdown
- [ ] Proposed solution documented
- [ ] Human acknowledged SCM-C limitations
- [ ] Inline diff applied manually
- [ ] Follow-up issue/PR linked
```

### Inline Diff Snippet

```diff
--- a/path/to/file.ext
+++ b/path/to/file.ext
@@
-old line
+new line
```

Application notes:

1. Save the snippet above to `change.diff`.
2. Run `git apply change.diff` from the repo root.
3. Inspect the result (`git diff`) before staging.

> Tip: For Markdown-only tweaks, copy the diff into the GitHub web editor and apply manually if `git apply` is unavailable.

## Maintenance Notes

- Review this page when the engineering contract’s SCM section changes.
- Update templates if new sections are added to plan/PR bodies or review formats.
- Reference `docs/design/ENGINEERING_CONTRACT.md` and `AGENTS.md` when scripting onboarding prompts.
