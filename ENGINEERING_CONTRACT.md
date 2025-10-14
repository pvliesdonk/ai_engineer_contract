# ENGINEERING_CONTRACT.md (AI × Peter) — v1.6.0

Owner: Peter van Liesdonk (`pvliesdonk`)
Purpose: Consistent, auditable collaboration on software and docs.

This is the canonical contract. Keep a copy at the repo root and reflect it in the ChatGPT Project prompt.

---

## 1) Branches & Flow
- Work under `pvliesdonk/{repo_name}`.
- `main` = releases only (via `<BASE_BRANCH> → main` when requested).
- **Default base branch:** `develop` (Git-Flow convention). Repos already using `development` are allowed; tools must accept `BASE_BRANCH=development` to target it.
- Feature branches: `feat/<slug>`, `fix/<slug>`, `docs/<slug>`, `chore/<slug>`, `refactor/<slug>`, `test/<slug>`.
- Always rebase on `origin/<BASE_BRANCH>` before PR. Squash-merge PRs into `<BASE_BRANCH>`.

## 2) PR Quality
- Conventional Commit title (`feat:`, `fix:`, …).
- Body: **Summary**, **Why**, **Changes**, **Validation**, **Risk & Rollback**, **Notes**.
- Small, focused diffs; update docs/tests alongside behavior changes.

## 3) Releases
- PR `<BASE_BRANCH> → main` titled `release: vX.Y.Z`. After merge: tag `vX.Y.Z` and create a GitHub Release (automated via release-please).

## 4) Access Modes
- With GitHub write access: operate directly.
- Without write access: deliver a **single-file PR script** using `git` + `gh` that branches from `origin/<BASE_BRANCH>`, applies embedded changes, **creates missing labels**, and opens a PR to `<BASE_BRANCH>`.

## 5) Artifact Delivery
- **Default:** Every deliverable (scripts, long diffs, docs) must be provided as a **downloadable file** in chat. Short scripts may also be shown inline; long ones can be hidden but still downloadable.
- **Advice-only mode (NEW):** If the user explicitly asks for *advice*, provide guidance/snippets/commands inline **without** packaging downloads. Return to the default download behavior for subsequent deliverables unless advice-only is requested again.
- Always include a one‑paragraph synopsis and **exact run command(s)** for each deliverable.

## 6) Robust Delimiters & Escaping
- Use raw triple‑quoted strings (`r"""..."""`), normalize to LF line endings, prefer base64 for binary/fragile payloads, and single‑quoted heredocs (`<<'EOF'`). Optional SHA‑256 verification for payloads.

## 7) Security
- No secrets in repos or logs. Use `.env.example`; ignore real secrets via `.gitignore`. Redact sensitive values in logs/PRs.

## 8) Communication
- Concise progress logs; deterministic scripts; pin versions where sensible.

## 9) Non‑Programming Repos
- Same PR/review flow. Validation adapts (link checkers, Markdownlint, MkDocs/mdBook, etc.).

## 10) New Repo Bootstrap
- **Confirm LICENSE** first (default **MIT**). Create `LICENSE`, `README.md`, `CONTRIBUTING.md`, minimal `.gitignore`. Create/push `main` and `<BASE_BRANCH>`. Ensure default labels exist.

## 11) Canonical Source & Distribution
- Canonical repo: `pvliesdonk/ai_engineer_contract`.
- Every new repo must include the **latest** `ENGINEERING_CONTRACT.md` and `tools/`:
  - `tools/pr_from_diff_TEMPLATE.py`
  - `tools/repo_bootstrap_TEMPLATE.py`
- Distribution choices: copy at creation, template repo, or git subtree for `tools/` (avoid submodules unless strictly needed).

## 12) Labels
- Commits/PRs must include appropriate labels. Scripts **auto-create** missing labels via `gh label create`.

## 13) Auto‑Upgrade in Chat
- When a newer contract or tool appears in the current chat/project, the AI must immediately use the newest version.

## 14) Auto‑Update Repositories
- When newer contract/tools exist in chat, the AI opens a PR that **replaces** `ENGINEERING_CONTRACT.md` and `tools/*` (unless the user opts out).
- PR title: `chore: sync canonical contract/tools to v<version>`; labels: `from-ai`, `needs-review`, `docs`.

## 15) TODOs & Not‑Implemented Stubs
- When stubbing behavior in code, **always** include explicit TODO markers and fail fast:
  - Python: `# TODO:` and `raise NotImplementedError("TODO: …")` (or `warnings.warn(..., NotImplementedWarning)` when non‑fatal).
  - JS/TS: `// TODO:` and `throw new Error("TODO: …")` (or guarded `console.warn` + early return).
  - Other languages: `TODO:` comments + explicit runtime error/exception where feasible.
- Place TODOs at the call site and/or function body so tests catch them early.

## 16) Conventional Commit Proposals (NEW)
- After every deliverable, the AI proposes **1–3** candidate **Conventional Commit** messages for the squash merge, plus a PR title, matching the change scope (e.g., `docs(contract): …`, `feat(tools): …`, `chore(ci): …`).

---

### Suggested Labels (auto‑created if absent)
`from-ai`, `needs-review`, `blocked`, `security`, `breaking-change`, `docs`, `chore`, `content`, `design`, `asset`

---

### Changelog
- v1.6.0 — Advice‑only mode; propose Conventional Commit messages after each deliverable.
- v1.5.0 — `develop` default + `BASE_BRANCH` override; TODO stubs required.
- v1.4.0 — Always-download rule; auto-upgrade in chat; auto-sync repos.
- v1.3.0 — Canonical distribution + tools.
- v1.2.0 — Repo bootstrap (license confirmation, CONTRIBUTING, labels).
- v1.1.0 — Robust escaping; auto-labels; non‑code repos.
- v1.0.1 — Deliverables downloadable.
- v1.0.0 — Initial.
