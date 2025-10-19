doc_type: architecture
doc_version: 2025-10-18.r1
---

Governance Artifacts Architecture
=================================

Overview
--------

This update introduces three governance-oriented components:

- A **Pre-Build Discipline** section embedded in the engineering contract that
  spells out allowed/disallowed agent actions prior to “GO BUILD” and references
  a PR checklist requirement.
- A **Decision Elicitation Protocol** paired with a repository-wide decision log
  (`docs/design/DECISIONS.md`) plus optional structured entries in
  `docs/design/decisions/`.
- An expanded **AGENTS.md baseline** that enumerates mandatory sections and
  provides a snippet agents can reuse.

Contract Updates
----------------

- Insert a `### Pre-Build Allowed Work` subsection under “## 18) Requirements & Design Phase”
  detailing permissible activities, prohibited actions, and checklist copy.
- Add a new numbered section “Decision Elicitation Protocol” outlining the one-at-a-time
  questioning approach, logging expectations, and acceptable storage locations.
- Extend “## 24) AGENTS.md Convention” with the mandatory headings list and inline template.

Documentation & Templates
-------------------------

- Create `docs/design/DECISIONS.md` (and optional `docs/design/decisions/*.yaml`) to record
  each decision’s question, chosen option, rationale, owner, and timestamp.
- Add `templates/docs.design.decisions_template.md` offering a starter table and YAML guidance.
- Update `AGENTS.md` to match the new baseline (explicit contract link, planning references,
  GO BUILD reminder, CI/labels, secrets policy, SCM handling).

Processes & Tooling
-------------------

- Require PRs that touch requirements/design to include the pre-build checklist section.
- Encourage agents to log decisions during requirements/design conversations and attach the log
  (or specific entries) to related issues/PRs.
