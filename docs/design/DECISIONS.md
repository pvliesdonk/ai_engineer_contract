---
doc_type: decisions_log
doc_version: 2025-10-18.r1
title: Decisions Log
---

| Date       | ID                | Prompt                                                               | Choice                                                                                  | Rationale                                                                                               | Linked Artifacts                                             |
| ---------- | ----------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| 2025-10-18 | D2025-10-18-01    | What work may agents perform before receiving “GO BUILD”?           | Adopt explicit allowed vs disallowed lists plus a PR checklist for pre-build submissions | Resolves ambiguity noted in #42; aligns repo operations with contract-first discipline.                  | docs/design/ENGINEERING_CONTRACT.md, issue #42               |
| 2025-10-18 | D2025-10-18-02    | How should agents elicit and track decisions during requirements?   | Introduce Decision Elicitation Protocol + required DECISIONS.md log with optional YAML   | Ensures auditable, automation-friendly decisions trail as requested in #43.                             | docs/design/ENGINEERING_CONTRACT.md, templates/…, issue #43  |
| 2025-10-18 | D2025-10-18-03    | What baseline content must AGENTS.md include across repositories?   | Mandate contract link, planning refs, GO BUILD gate, CI/labels, secrets, SCM mode section | Standardizes operator onboarding and reduces misconfiguration risk per #44.                              | docs/design/ENGINEERING_CONTRACT.md, AGENTS.md, issue #44    |
