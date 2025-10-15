# ENGINEERING_CONTRACT.md (AI × Peter) — v1.6.4

Owner: Peter van Liesdonk (`pvliesdonk`)
Purpose: Consistent, auditable collaboration on software and docs.

This is the canonical contract. Keep a copy at the repo root and reflect it in the ChatGPT Project prompt.

---

## 1) Branches & Flow
- Work under `pvliesdonk/{repo_name}`.
- `main` = releases only (cut from `<BASE_BRANCH> → main` when requested).
- **Development branch (`<BASE_BRANCH>`):** default is `develop` (Git-Flow). Repos using `development` are supported via `BASE_BRANCH=development`. The repo’s *GitHub default branch* may remain `main`.
- Feature branches: `feat/<slug>`, `fix/<slug>`, `docs/<slug>`, `chore/<slug>`, `refactor/<slug>`, `test/<slug>`.
- Always rebase on `origin/<BASE_BRANCH>` before PR. Squash-merge PRs into `<BASE_BRANCH>`.

## 2) PR Quality
- Title must be a **Conventional Commit** (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `ci:`, `test:`). Add `!` for breaking changes.
- Body includes: **Summary**, **Why**, **Changes**, **Validation**, **Risk & Rollback**, **Notes**.
- Small, focused diffs; update docs/tests with behavior changes.

## 3) Releases & Automation (Tool-Agnostic)
We use a **Release Automation Tool (RAT)** to generate versions, tags, release notes, and (optionally) `CHANGELOG.md`. Acceptable tools include, but are not limited to, **release-please**, **semantic-release**, or equivalent.

**Requirements for the RAT:**
- Parse **Conventional Commits** to produce SemVer bumps, release notes, and (if used) `CHANGELOG.md`.
- Prefer a **Release PR** (reviewable). Bot commits on **`main`** are allowed but discouraged unless required.
- Create a **Git tag** and **GitHub Release** on merge/approval.
- Be configurable for our flow (base branch is `<BASE_BRANCH>`; release branch is `main`).

**Back-merge rule (Git-Flow integration):**
- After a release is created on `main`, **back-merge `main → <BASE_BRANCH>`** (PR or automation) so development carries the released **CHANGELOG/version artifacts**. If a hotfix also landed on `main`, include it and **note it** in the PR body.
- Do **not** hand-edit `CHANGELOG.md` on `<BASE_BRANCH>`; the RAT owns release artifacts. Resolve conflicts by favoring `main`’s generated content.

**No RAT scenario (temporary):**
- The AI drafts a Conventional-Commit–derived changelog section in the PR and updates `CHANGELOG.md` as part of that PR. Once a RAT is enabled, its output becomes the source of truth.

## 4) Access Modes
- With GitHub write access: operate directly.
- Without write access: deliver a **single-file PR script** (`git` + `gh`) that branches from `origin/<BASE_BRANCH>`, applies embedded changes, **creates missing labels**, and opens a PR to `<BASE_BRANCH>`.

## 5) Artifact Delivery
- **Default:** Every deliverable (scripts, long diffs, docs) must be provided as a **downloadable file** in chat. Short scripts may also appear inline; long ones can be hidden but must be downloadable.
- **Advice-only mode:** If the user explicitly asks for *advice*, provide guidance/snippets/commands inline **without** packaging downloads. Scope is **this request only**, unless the user explicitly asks to keep advice-only for a larger task/thread.
- Always include a one-paragraph synopsis and **exact run command(s)** for each deliverable.

## 6) Robust Delimiters & Escaping
- Use raw triple-quoted strings (`r"""..."""`), normalize to LF line endings, prefer base64 for binary/fragile payloads, and single-quoted heredocs (`<<'EOF'`). Optional SHA-256 verification for payloads.

## 7) Security
- No secrets in repos or logs. Use `.env.example`; ignore real secrets via `.gitignore`. Redact sensitive values in logs/PRs.

## 8) Communication
- Concise progress logs; deterministic scripts; pin versions where sensible.

## 9) Non-Programming Repos
- Same PR/review flow. Validation adapts (link checkers, Markdownlint, MkDocs/mdBook, etc.).

## 10) New Repo Bootstrap
- **Confirm LICENSE** first (default **MIT**). Create `LICENSE`, `README.md`, `CONTRIBUTING.md`, minimal `.gitignore`. Create/push `main` and `<BASE_BRANCH>`. Ensure default labels exist.

## 11) Canonical Source & Distribution
- Canonical repo: `pvliesdonk/ai_engineer_contract`.
- Every new repo must include the **latest** `ENGINEERING_CONTRACT.md` and `tools/`.
- Distribution choices: link to canonical, copy at creation, or sync via tool/subtree (avoid submodules unless strictly needed).

## 12) Labels
- Commits/PRs must include appropriate labels. Scripts **auto-create** missing labels via `gh label create`.
- **Definitive list:** `from-ai`, `needs-review`, `docs`, `chore`, `security`, `blocked`, `breaking-change`, `content`, `design`, `asset`, `deviation-approved`.

## 13) Auto-Upgrade in Chat
- When a newer contract or tool appears in the current chat/project, the AI must immediately use the newest version.

## 14) Auto-Update Repositories
- When newer contract/tools exist in chat, the AI opens a PR that updates `ENGINEERING_CONTRACT.md` and **replaces only canonical** `tools/canonical/*` files (unless the user opts out). Preserve `tools/local/*`; if conflicts exist, surface them explicitly in the PR body.

## 15) TODOs & Not-Implemented Stubs
- When stubbing behavior in code, **always** include explicit TODO markers and fail fast:
  - Python: `# TODO:` and `raise NotImplementedError("TODO: …")` (or `warnings.warn(..., NotImplementedWarning)` when non-fatal).
  - JS/TS: `// TODO:` and `throw new Error("TODO: …")` (or guarded `console.warn` + early return).
  - Other languages: `TODO:` comments + explicit runtime error/exception where feasible.
- Place TODOs at the call site and/or function body so tests catch them early.

## 16) Conventional Commit Proposals
- After every deliverable, the AI proposes **1–3** candidate **Conventional Commit** messages for the squash merge, plus a PR title, matching the change scope (e.g., `docs(contract): …`, `feat(tools): …`, `chore(ci): …`).

## 17) Changelog & Release Notes
- **Source of truth:** The **RAT** (release automation tool) generates release notes and, if configured, `CHANGELOG.md`. Do not edit generated changelog entries by hand.
- **Flow:** Release on `main` → back-merge `main → <BASE_BRANCH>` to carry artifacts back into development.
- **Fallback:** If no RAT is enabled, the AI or contributor must update `CHANGELOG.md` in the PR (following Conventional Commits).

## 18) Deviation Protocol (Ask-to-Derive)
- The AI may **request permission to deviate** from any clause when there is a strong reason (policy conflict, security risk, compliance, branch protections, repo layout constraints).
- The request must include: **(a) reason**, **(b) scope/impact**, **(c) alternatives**, **(d) rollback plan**. **Approval** is required from **Peter** (or a **CODEOWNER**).
- Once approved, add label **`deviation-approved`**, document it in the PR body, and—if user-visible—note it in `CHANGELOG.md`.

## 19) Tooling Policy (Optional by Design)
- The tools in `tools/` are **reference implementations** (optional). The AI may use alternative tooling if it meets these capabilities:
  1) **Reproducible**: idempotent runs; deterministic output.
  2) **Correct base**: branches from `origin/<BASE_BRANCH>` head; rebases cleanly. Use **`BASE_BRANCH`** as the environment knob (standard).
  3) **Safe PRs**: opens PRs with labels; never force-push to protected branches.
  4) **Escaping & integrity**: robust delimiting; optional SHA-256 for embedded artifacts.
  5) **Audit trail**: clear logs; proposed Conventional Commit messages.
  6) **Dry-run** mode or equivalent preview where feasible.
- If bring-your-own tooling is used, the PR must state **which tool** ran and confirm it satisfies the above. Canonical tools may live under `tools/canonical/*`; local extensions under `tools/local/*` to avoid sync collisions.

---

### Changelog
- v1.6.4 — Clarify advice-only scope; define `<BASE_BRANCH>`; prefer Release PR; narrow back-merge scope; approver+label for deviations; optional tooling requirements; canonical vs local tools; consolidate labels.
- v1.6.3 — Deviation Protocol + Tooling Policy (optional by design).
- v1.6.2 — Tool-agnostic releases; keep back-merge rule; clarify changelog ownership.
- v1.6.1 — Document back-merge main→base and changelog ownership.
- v1.6.0 — Advice-only mode; propose Conventional Commit messages after each deliverable.
- v1.5.0 — `develop` default + `BASE_BRANCH` override; TODO stubs required.
- v1.4.0 — Always-download rule; auto-upgrade in chat; auto-sync repos.
- v1.3.0 — Canonical distribution + tools.
- v1.2.0 — Repo bootstrap (license confirmation, CONTRIBUTING, labels).
- v1.1.0 — Robust escaping; auto-labels; non-code parity.
- v1.0.1 — Deliverables downloadable.
- v1.0.0 — Initial.
