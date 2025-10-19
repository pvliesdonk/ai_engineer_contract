---
doc_type: kb_page
doc_version: 2025-10-18.r1
title: Quality Bar Linter Specification
---

Quality Bar Linter Specification
================================

Intent
------

- Encode the repository “Quality Bar” into a repeatable linter that can run locally and in CI.
- Provide a portable checklist repositories can adopt in warn-only mode and later promote to a blocking gate.
- Reference: Section 27 of `docs/design/ENGINEERING_CONTRACT.md`.

Checks
------

The Quality Bar linter MUST validate at least the following:

1. **Front matter ⇔ H1 alignment** – The document title in YAML front matter matches the first H1.
2. **Status line present** – Documents that require status (e.g., roadmap, ADRs) include the status field and valid value.
3. **Section completeness** – Skeleton sections (e.g., “TODO”, “TBD”) are disallowed unless explicitly permitted by the contract.
4. **Link audit** – No broken relative links inside `docs/`; prefer `markdown-link-check` or a comparable tool in dry-run mode.
5. **Citation hygiene** – References must include source identifiers (URL, ISBN, etc.) and page spans when quoting physical media.

Implementation Guidance
-----------------------

- Start with a composite script (Python or Node) that orchestrates existing tools (markdownlint, regex checks, link checkers).
- Stage the linter in CI with **warn-only** output during requirements/design phases; flip to blocking once the repository reaches the “build” phase.
- Surface remediation hints in CI output to accelerate fixes.

CLI Skeleton (Python Example)
-----------------------------

```python
# quality_bar.py
```

- Implement each check as a function returning a list of violations.
- Exit code `0` when `--warn-only` is set; return `1` otherwise.

CI Integration
--------------

- Add a dedicated workflow (e.g., `.github/workflows/quality-bar.yml`) running on pull requests.
- During early adoption set `warn-only` to avoid blocking merges; switch to strict mode once the team confirms stability.
- Reference this document and the Engineering Contract quality section in the workflow description.

Adoption Playbook
-----------------

1. Document the selected implementation (Python, Node) in the repo’s README/CONTRIBUTING.
2. Communicate the rollout phases (warn-only → blocking) to contributors.
3. Store custom configuration under `tools/quality_bar/` or similar for reuse.
4. Periodically audit the linter to ensure the Quality Bar remains aligned with contract updates.
