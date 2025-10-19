doc_type: requirements
doc_version: 2025-10-19.r1
---

Governance & Operator Guidance (P0)
===================================

This iteration focuses on codifying the operator guardrails that repeatedly surfaced in issues
[#42](https://github.com/pvliesdonk/ai_engineer_contract/issues/42),
[#43](https://github.com/pvliesdonk/ai_engineer_contract/issues/43), and
[#44](https://github.com/pvliesdonk/ai_engineer_contract/issues/44).

R1 — Pre-Build Discipline
------------------------

- Define explicit categories of work that are allowed before a Plan issue unlocks implementation.
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
- Mandate sections covering contract link, planning docs, plan/build gate, labels/CI, secrets policy,
  and session-mode handling.
- Supply a snippet/template agents can copy when authoring repository-specific instructions.
- Update this repository’s root `AGENTS.md` to comply with the new baseline.

R4 — Quality Bar Enforcement & SCM Guidance
-------------------------------------------

- Define a Quality Bar linter spec that checks heading alignment with YAML, status lines,
  section completeness, link references, and citation presence.
- Document when the linter should run (warn-only vs mandatory) and how to integrate it into CI.
- Expand session capability mode (SCM) guidance with detection steps, confirmation prompts,
  and a matrix of allowed operations per mode.
- Provide a decision tree for agents to follow before performing SCM-impacting tasks.

R5 — IP Rights & Dual-Role Documentation
----------------------------------------

- Add a rights attestation template to the IP disclaimer guidance covering quotation allowances,
  copyright terms, and required citation spans.
- Provide a reusable `templates/docs.kb.ip_disclaimer_template.md` file mirroring the guidance.
- Create `docs/kb/dual-role.md` differentiating canonical distribution assets from instance-only
  workflows, templates, and scripts. Link to it from the README and relevant docs.
- Annotate instance-only GitHub workflows with header comments explaining their scope.
- Highlight directory conventions (e.g., `tools/*_TEMPLATE.py` canonical vs potential local-only
  scripts living under `tools/local/`).

R6 — Tool Template Portability
------------------------------

- Update `tools/sync_canonical_contract_and_tools_TEMPLATE.py`,
  `tools/pr_from_diff_TEMPLATE.py`, and `tools/repo_bootstrap_TEMPLATE.py` to derive owner/repo
  information from the repo manifest or Git remotes by default, while preserving CLI/env overrides.
- Ensure updated scripts document the overrides and pass `python -m py_compile`.
- Refresh README/tool docstrings to describe the new behavior.
