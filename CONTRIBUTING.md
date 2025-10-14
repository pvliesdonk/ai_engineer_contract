# Contributing

This repository is governed by **ENGINEERING_CONTRACT.md** (canonical). Read it first.

## Branches

- `main` — releases only.
- **Base branch** for development is `develop` (Git-Flow convention).
  - Repositories that already use `development` are supported; tools accept `BASE_BRANCH=development` to target it.

## Conventional Commits

All commits and squash-merge titles must follow **Conventional Commits**:

- `feat(scope): add capability` — user-visible feature
- `fix(scope): correct behavior` — bug fix
- `docs(scope): update docs/contract` — documentation
- `chore(scope): maintenance` — non-user-visible changes
- `ci(scope): workflow/automation` — CI/CD
- `refactor(scope): internal change` — no behavior change
- Add `!` for breaking changes, e.g. `feat!: ...`

Assistants propose **1–3** candidate messages after each deliverable.

## Pull Requests

- Branch from `origin/<BASE_BRANCH>` (default `develop`) and **rebase** before opening a PR.
- Keep diffs focused and include docs/tests for behavior changes.
- Structure the body:
  - **Summary** — one paragraph
  - **Why**
  - **Changes**
  - **Validation** — how it was tested
  - **Risk & Rollback** — what can go wrong/how to revert
  - **Notes**
- Squash-merge with a Conventional Commit title.
- Labels: ensure PRs carry meaningful labels (`from-ai`, `needs-review`, `docs`, etc.). Tools auto-create labels if missing.

## Deliverables & Advice-only

- By default, deliverables (scripts, long diffs, docs) must be provided as **downloadable files**.
- When the user explicitly asks for **advice**, provide guidance/snippets inline **without** packaging downloads.

## Security

- Never commit secrets. Use `.env.example` and ignore real secrets.
- Redact sensitive values in logs and PRs.

## Releases

- `release-please` opens a **Release PR** from Conventional Commits.
- Merge the Release PR to create the tag and GitHub Release.

