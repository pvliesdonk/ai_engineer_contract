doc_type: architecture
doc_version: 2025-10-18.r2
---

Governance Artifacts Architecture
=================================

Overview
--------

This iteration layers on operational governance (Quality Bar enforcement and SCM mode rules),
dual-role documentation, IP rights guidance, and tooling portability improvements.

Contract Updates
----------------

- Append a **Quality Bar Enforcement** section describing the linter checks, adoption phases
  (warn-only vs blocking), and CI expectations.
- Enhance the **Session Capability Modes** area with detection steps, confirmation prompts, and
  allowed operations per mode, backed by a decision tree reference.
- Expand **AGENTS.md Convention** to mention the new dual-role guidance and references to the
  Quality Bar/SCM sections.
- Reference the rights attestation template and dual-role doc in the appropriate contract sections.

Documentation & Templates
-------------------------

- Add `docs/kb/dual-role.md` mapping canonical vs instance assets, pointing to workflow annotations
  and directory conventions.
- Introduce an IP disclaimer template snippet covering rights attestation via
  `docs/kb/howtos/ip-disclaimer.md` and ship `templates/docs.kb.ip_disclaimer_template.md` for reuse.
- Update `ai/session-mode-handshake.md` with the detection/confirmation flow and link to the
  decision tree.
- Extend README to surface the dual-role doc and mention the Quality Bar/SCM resources.

Processes & Tooling
-------------------

- Document the Quality Bar linter spec in `docs/kb/howtos/quality-bar-linter.md` (new) and outline
  how repositories should integrate or phase it in.
- Update GitHub workflow YAML headers to call out instance-only behavior for this repo.
- Modify tool templates to autodetect owner/repo using `ai/manifest.json` or Git remotes while
  keeping CLI/env overrides; ensure docstrings and README guidance reflect the changes.
- Maintain decision logs for each change driver (issues #46, #47, #49, #55, #57).
