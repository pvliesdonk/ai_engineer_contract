# AGENTS.md — AI Agent Instructions (repo-wide)

This file defines how coding agents should operate in this repository. It follows the agents.md convention: a root `AGENTS.md` applies to the entire repo; more deeply nested `AGENTS.md` files may refine/override within their subtree; direct instructions from a human always take precedence.

Scope: Entire repository.

## Dual-Role Awareness

- This repository hosts the generic engineering contract and also applies the contract to itself.
- Treat `docs/design/ENGINEERING_CONTRACT.md` as tool-agnostic guidance for consumers; workflows in this repo are examples, not mandates.

## High‑Level Rules

- Base branch: `develop` (sole development branch). `main` is for releases.
- Branching: create topic branches from `origin/develop` using `feat/<slug>`, `fix/<slug>`, `docs/<slug>`, `chore/<slug>`, `refactor/<slug>`, `test/<slug>`.
- PRs: target `develop`. Squash‑merge after review/approval. Keep diffs small and focused.
- Conventional Commits: required for PR titles. Use `!` for breaking changes.
- Releases: managed by release automation (release‑please). Release PRs target `main`. After a release, back‑merge `main → develop` to carry changelog/version.

## Files & Layout

- Contract: `docs/design/ENGINEERING_CONTRACT.md` (authoritative engineering contract). Keep it updated and link to it in PRs.
- Design docs: `docs/design/` (requirements, architecture, ADRs, roadmap). Knowledge base/wiki: `docs/kb/` with an `index.md`.
- AI manifest: `ai/manifest.json` (paths, base branch, labels, doc versioning scheme).
- Doc versioning: use `date+rev` in YAML front matter for design/kb documents; releases use SemVer.

## Tooling & CI

### Phase Gates

- The repo uses `phase.yaml` and `.github/workflows/phase-gate.yml` to enforce path allowlists per phase.
- Defaults: requirements/design allow `docs/**`, `AGENTS.md`, `ai/**`, `phase.yaml`; plan adds `.github/**`; build is unrestricted.
- To advance phases, submit a separate PR updating `phase.yaml`. For temporary deviations, add `deviation-approved` with rationale.

- Use `git` and `gh` for operations (clone/branch/push/PR/labels). Prefer release‑please for versioning and changelog.
- Linting: Markdown lint runs in CI (markdownlint‑cli2). Follow `.markdownlint-cli2.yaml` and `.markdownlintignore`.
- Markdown formatting: satisfy common rules locally to avoid CI failures — add a blank line before and after headings (MD022) and before/after lists (MD032).
- Validate Python helper scripts by byte‑compiling them (`python -m py_compile tools/*.py`) when applicable.
- AI CI tool selection: When generating code or scripts, wire minimal CI appropriate to the stack in the same PR. Examples:
  - Python: ruff/flake8 or equivalent, black/format check, `python -m py_compile`, and a basic `pytest -q` smoke if tests exist.
  - Node/TS: eslint + prettier checks, typecheck (tsc) if TS, and a basic `npm test -s` smoke when present.
  - Shell: shellcheck.
  - Docs-only: markdownlint.
  - Add others as needed (Go: golangci-lint; Rust: cargo fmt/clippy/test; Terraform: fmt/validate; Docker: hadolint).

## Labels & Management

- Ensure these labels exist (auto‑create if missing): `from-ai`, `needs-review`, `docs`, `chore`, `security`, `blocked`, `planning`, `needs-design-ref`, `breaking-change`, `content`, `design`, `asset`, `deviation-approved`.
- Link PRs to issues; reference relevant design docs. If design impact exists and the doc isn’t ready, add `needs-design-ref` and follow up with the doc.

- Feedback channel: when ambiguity is detected in the canonical contract or tools, open an issue on the canonical repo with labels `feedback`/`question`, referencing the exact doc section.

## Security & Secrets

- Do not commit secrets. Use `.env.example`; real secrets must remain out of the repo/CI logs. Redact tokens in PRs and outputs.

## Session Modes (awareness)

- SCM‑A (Full‑Stack Agent): may create branches/PRs/issues/labels; merge to `develop` only after explicit chat approval; releases to `main` are manual.
- SCM‑B (IDE Co‑Driver): edits files, proposes ready‑to‑run commands, but cannot push; provide precise instructions/scripts.
- SCM‑C (Chat‑Only): use single‑file templates in `tools/` to open PRs (copy‑paste friendly flows).

## Communication & Process

- Be concise. Provide progress updates and explicit next steps. Propose 1–3 Conventional Commit messages for meaningful deliverables.
- For fragile payloads, use robust delimiters (heredocs/base64) and verify with checksums when warranted.
- Deviations from this policy require approval and the `deviation-approved` label; document rationale and rollback plan.

### Issue Hygiene & Proposal Tracking

- Open issues for next steps and link to relevant design/KB sections.
- When working an issue, post a “Proposed solution” comment summarizing scope, approach, acceptance criteria, risks/rollback, and CI considerations (e.g., phase vs harness alignment). Update it if plans change and reference it from the PR body.

## Quick Reference (for agents)

- Base: `develop`; PR target: `develop`; release PR target: `main`.
- Contract path: `docs/design/ENGINEERING_CONTRACT.md`.
- Design roots: `docs/design/`; KB root: `docs/kb/`.
- Run markdown lint via CI; keep docs consistent with changes.
- Syncing canonical contract (consumers): use `tools/sync_canonical_contract_and_tools_TEMPLATE.py` with `--dry-run` and pin to a release tag; avoid `--force` unless necessary. See `docs/kb/howtos/sync-canonical.md` and `ai/sync.config.json`.
