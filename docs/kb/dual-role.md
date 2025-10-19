---
doc_type: kb_page
doc_version: 2025-10-18.r1
title: Dual Role – Canonical vs Instance Assets
---

Dual Role – Canonical vs Instance Assets
=======================================

Intent
------

- Explain how this repository simultaneously distributes the canonical Engineering Contract and hosts an instance customised for `pvliesdonk/ai_engineer_contract`.
- Help consumers identify which files can be copied verbatim and which are examples that should be adapted.

Asset Map
---------

| Area                          | Canonical (Copy As-Is)                                             | Instance (Example Only)                                               |
| ----------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------- |
| Contract & Capsule            | `docs/design/ENGINEERING_CONTRACT.md`, `ai/contract_capsule.md`    | N/A                                                                   |
| Design templates              | `templates/docs.design.*`                                          | Local ADRs, requirements, architecture specific to this repo          |
| Tool templates                | `tools/*_TEMPLATE.py`                                              | Future `tools/local/` scripts (if introduced)                         |
| Workflows                     | `.github/workflows/examples/*.yml`                                 | `.github/workflows/*.yml` (annotated as instance-specific)            |
| Knowledge base                | `docs/kb/howtos/*` templates                                       | `docs/kb/dual-role.md`, repo-specific how-tos and guides              |
| Automation configs            | `.markdownlint-cli2.yaml`, `.markdownlintignore`                   | release-please settings tied to this repo’s cadence                   |

Workflow Annotation
-------------------

- All instance workflows now carry a header comment noting they exist for this repository.
- Consumers should start from the examples under `.github/workflows/examples/` and adapt them to their stack and release automation.

Directory Conventions
---------------------

- Canonical tool templates remain under `tools/` with the `_TEMPLATE.py` suffix.
- If the instance needs custom scripts, place them under `tools/local/` (not currently present) to avoid confusion with distributable templates.

Further Reading
---------------

- [Quality Bar Linter Specification](./howtos/quality-bar-linter.md)
- [IP Rights & Attestation Template](./howtos/ip-disclaimer.md)
