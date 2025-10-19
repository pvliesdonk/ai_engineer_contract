# Contract Capsule v2.1.2

- Base: `develop`; PRs → `develop`; squash; Conventional Commit titles.
- Do NOT code until requirements + design are updated/approved. Wait for “GO BUILD”.
- Keep docs in `docs/design` and `docs/kb` updated with changes.
- Branching: `feat|fix|docs|chore|refactor|test/<slug>`; chain branches for milestones; avoid conflicting parallel work.
- Early CI: fast lint/format + byte-compile/smoke; choose tools per stack (Python/Node/TS/Rust/etc.).
- Docs as core deliverable: use Conventional Commits to drive SemVer — breaking normative change (`docs(contract)!` + BREAKING CHANGE footer), new capability (`feat(contract)`), clarification (`fix(contract)`). For docs-only tags, add `Release-As: x.y.z`.
- No secrets. Use `.env.example`. Redact tokens.
- Releases via RAT; here: release-please; back-merge `main → develop`.
- Labels: `from-ai`, `needs-review`, `docs`, `chore`, …
- Provide progress updates; propose 1–3 Conventional Commit messages after deliverables.

Reference: `docs/design/ENGINEERING_CONTRACT.md` (v2.1.2), `ai/manifest.json`.

Acknowledge with: `ACK CONTRACT v2.1.2`. Detect SCM mode once.
