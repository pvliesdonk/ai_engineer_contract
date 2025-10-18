doc_type: requirements
doc_version: 2025-10-18.r1
---

Governance & Operator Guidance (P0)
===================================

This iteration focuses on codifying the operator guardrails that repeatedly surfaced in issues
[#42](https://github.com/pvliesdonk/ai_engineer_contract/issues/42),
[#43](https://github.com/pvliesdonk/ai_engineer_contract/issues/43), and
[#44](https://github.com/pvliesdonk/ai_engineer_contract/issues/44).

R1 — Pre-Build Discipline
------------------------

- Define explicit categories of work that are allowed before a human issues “GO BUILD”.
- List disallowed activities (e.g., creating code files, scaffolding tests) with illustrative examples.
- Add a lightweight PR checklist agents must include when submitting pre-build changes.
- Ensure guidance lives in `docs/design/ENGINEERING_CONTRACT.md` and references the checklist.

R2 — Decision Elicitation Protocol
----------------------------------

- Capture a canonical protocol for asking one-at-a-time questions with recommended defaults.
- Require repositories to maintain `docs/design/DECISIONS.md` that logs prompts, selected options,
  rationale, and dates. Allow optional per-decision YAML files in `docs/design/decisions/`.
- Provide a reusable template (under `templates/`) for the decisions log.
- Cross-reference the protocol from the engineering contract and README/KB where applicable.

R3 — AGENTS.md Baseline
-----------------------

- Elevate AGENTS.md content requirements into the engineering contract.
- Mandate sections covering contract link, planning docs, GO BUILD gate, labels/CI, secrets policy,
  and session-mode handling.
- Supply a snippet/template agents can copy when authoring repository-specific instructions.
- Update this repository’s root `AGENTS.md` to comply with the new baseline.
