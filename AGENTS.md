# AGENTS.md — AI Agent Instructions (repo-wide)

This file defines how coding agents should operate in this repository. A root `AGENTS.md` applies repo-wide; nested files may refine rules for their subtree; human instructions override all.

## Contract Link & Scope

- Authoritative contract: [docs/design/ENGINEERING_CONTRACT.md](docs/design/ENGINEERING_CONTRACT.md)
- Base branch: `develop`; PRs target `develop`; releases cut via release-please on `main` then back-merge.
- Dual-role note: this repo publishes the canonical contract while applying it locally—treat workflows here as examples, not mandates for consumers.

## Planning Sources

- Requirements/design: `docs/design/` (`requirements.md`, `architecture.md`, `DECISIONS.md`, ADRs, roadmap).
- Knowledge base: `docs/kb/` with `index.md`; keep KB pages synced with shipped behavior.
- Maintain `docs/design/DECISIONS.md` (and optional `docs/design/decisions/*.yaml`) as decisions are made.

## GO BUILD Gate

- No code/tests/assets before an explicit “GO BUILD”.
- Pre-build changes are limited to docs/planning/ops work; follow the contract’s allowed/disallowed list.
- Include the pre-build checklist in every pre-build PR and check all boxes before requesting review.

## Branching, PRs & Labels

- Branch naming: `feat|fix|docs|chore|refactor|test/<slug>` off `origin/develop`.
- Rebase frequently; squash-merge after approval; link PRs to issues (`Fixes #ID`).
- Apply `from-ai`, `needs-review`, and scope labels (`docs`, `chore`, `design`, etc.). Ensure the standard label set exists.

## CI & Tooling

- Phase gates: `phase.yaml` + `.github/workflows/phase-gate.yml` gate paths per phase (requirements/design/docs-only). Advance phases via dedicated PRs; use `deviation-approved` only with documented rationale.
- Docs-only changes: run markdownlint; Python helpers must pass `python -m py_compile tools/*.py`.
- Add stack-appropriate lint/test checks when generating new code (see contract for tool selection guidance).
- Prefer `gh` for repo automation; run release-please manually via workflow dispatch until automation is restored (see docs/issues/2025-10-19-release-please-automation.md).

## Security & Secrets

- Never commit secrets; use `.env.example` for shape. Redact tokens/keys in outputs.
- Coordinate with maintainers for secret rotation; avoid storing credentials in CI logs or artifacts.

## Session Modes (SCM-A/B/C)

- Detect the active mode once, confirm capabilities with the human if unclear, and document any switch.
- **SCM-A:** full control (branches/PRs); merge to `develop` only with explicit approval; releases are manual.
- **SCM-B:** provide ready-to-run edits/scripts; human executes/pushes.
- **SCM-C:** rely on templates in `tools/` for copy/paste flows; keep instructions concise and auditable.
