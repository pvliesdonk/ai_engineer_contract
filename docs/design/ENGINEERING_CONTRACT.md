# ENGINEERING_CONTRACT.md (AI × Peter) — v2.0.0

> Breaking change: `<BASE_BRANCH>` is removed. The development branch is **always `develop`**.

## 1) Branches & Flow
- Work under `pvliesdonk/{repo_name}`.
- `main` = releases only (cut from `develop → main` when requested).
- **Development branch:** `develop` (no alternates).
- Feature branches: `feat/<slug>`, `fix/<slug>`, `docs/<slug>`, `chore/<slug>`, `refactor/<slug>`, `test/<slug>`.
- Always rebase on `origin/develop` before PR. Squash-merge PRs into `develop`.

## 2) PR Quality
- Title: **Conventional Commit** (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `ci:`, `test:`). Add `!` for breaking changes.
- Body: **Summary**, **Why**, **Changes**, **Validation**, **Risk & Rollback**, **Notes**.
- Small focused diffs; update docs/tests with behavior changes.

## 3) Releases & Automation (Tool-Agnostic)
- Use a **Release Automation Tool (RAT)** (e.g., release-please, semantic-release) to produce SemVer tags, release notes, and (optionally) `CHANGELOG.md`.
- Prefer a **Release PR** over direct bot commits on `main`.
- After release on `main`, **back-merge `main → develop`** so development carries release artifacts (changelog/version).

## 4) Session Capability Modes (SCM)
- **SCM-A — Full-Stack Agent:** direct access to code, `git`, `gh`, runtimes, and tokens. Do everything automatically (branches, commits, PRs, labels, issues, projects). Merge into **`develop`** after explicit chat approval. **Releases on `main` are always manual** (human presses the button).
- **SCM-B — IDE Co-Driver:** can edit files but cannot push. Provide ready-to-run scripts/patches and precise commands. Track readiness and tell the human when to merge or open release PRs.
- **SCM-C — Chat-Only Operator:** minimal environment. Use **single-file Python templates** in `tools/` to open PRs. Optimize for copy-pasteable steps and UI click-paths.
- Detect mode once per session; ask **once** if uncertain. Mode can be changed on request.

## 5) Artifact Delivery
- **Default:** Provide deliverables as **downloadable files**. Long scripts can be hidden in chat but must be downloadable.
- **Advice-only:** When explicitly asked for advice, give guidance/snippets/commands without packaging deliverables (scoped to the current request).

## 6) Robust Delimiters & Escaping
- Use raw triple-quoted strings, LF line endings, single-quoted heredocs (`<<'EOF'`), and base64 for fragile/binary payloads. Optional SHA-256 verification.

## 7) Security
- No secrets in repos or logs. Use `.env.example`; ignore real secrets via `.gitignore`. Redact in logs/PRs.

## 8) Communication
- Concise progress logs; deterministic scripts; pin versions where sensible.

## 9) Programming-Adjacent Projects (Docs/KBase/Wiki)
- The same PR/review flow applies. Validation adapts (link checkers, Markdownlint, doc build if any).
- **Docs live under `docs/`**. For knowledge bases, prefer **`docs/kb/`** with an **`index.md`** (front matter + TOC).
- Design docs (requirements/architecture/ADRs) live under **`docs/design/`**.
- **Versioning separation:** Releases use **SemVer**; design/kb docs use **date+revision** (`doc_version: YYYY-MM-DD.rN` in YAML front matter).
- Issues/PRs must link to the relevant doc sections; the AI may create issues/labels/milestones/projects.

## 10) New Repo Bootstrap
- Confirm LICENSE (usually **MIT**). Create `LICENSE`, `README.md`, `CONTRIBUTING.md`, minimal `.gitignore`. Create/push `main` and `develop`. Ensure default labels exist.

## 11) Canonical Source & Distribution
- Canonical repo: `pvliesdonk/ai_engineer_contract`. Keep the contract in consumer projects at `docs/design/ENGINEERING_CONTRACT.md` with a link back here.
- Include the latest contract and (optionally) `tools/` in new repos. You may sync updates via PR.

## 12) Labels
- Commits/PRs should have labels. Scripts **auto-create** missing labels via `gh label create`.
- Suggested labels: `from-ai`, `needs-review`, `docs`, `chore`, `security`, `blocked`, `planning`, `needs-design-ref`, `breaking-change`, `content`, `design`, `asset`, `deviation-approved`.

## 13) Auto-Upgrade in Chat & Repos
- When a newer contract/tool appears in the current chat, immediately use it.
- Open a PR to update `ENGINEERING_CONTRACT.md` and **replace only canonical** `tools/canonical/*` if you’re using them; keep `tools/local/*` intact.

## 14) TODOs & Not-Implemented Stubs
- Stubbed code must include explicit TODO markers and fail fast (language-appropriate `NotImplemented`/exceptions or warnings). Place TODOs at call sites and function bodies.

## 15) Conventional Commit Proposals
- After every deliverable, propose 1–3 candidate Conventional Commit messages and a PR title.

## 16) Changelog & Release Notes
- The **RAT** is the source of truth for release notes and `CHANGELOG.md` (if enabled). Don’t edit generated changelog entries by hand. If no RAT, PRs must update `CHANGELOG.md`.

## 17) Deviation Protocol
- Request permission to deviate: include reason, scope/impact, alternatives, rollback. Approval by **Peter** or a **CODEOWNER**. Label `deviation-approved`; document in the PR and changelog if user-visible.

## 18) Requirements & Design Phase
- Before building, perform requirements + design and commit docs to `docs/design/`:
  - `requirements.md`, `architecture.md`, `decision-log/ADR-YYYYMMDD-<slug>.md`
  - Optional: `test-plan.md`, `roadmap.md`, diagrams (commit sources).
- Update docs with each PR that changes behavior/scope.

## 19) Issue & Project Management (AI allowed)
- The AI may create issues/labels/milestones/projects. **Design-impacting work must link to design docs**, otherwise label `needs-design-ref` and add the doc before implementation.
- Link PRs to issues (`Fixes #123`). Avoid assigning people unless asked; prefer milestones/projects.

## 20) Planning vs Releases
- Plan by **Milestones** (`M1`, `M2`, …) and optional **Release Trains** (`RYYYY.MM`, `RYYYYQn`), not by future SemVer.
- Record the *actual* shipped tags **after** release in `docs/design/delivery-map.yml`.

## 21) Branching Discipline
- All work happens on a topic branch off `origin/develop` (`feat/<slug>`, `fix/<slug>`, etc.).
- Keep **many small commits**. Squash-merge into `develop`.
- Keep branches **rebased** on `origin/develop`. Do **not** delete topic branches until the change is released and back-merged (`main` → `develop`).

## 22) Merge-Readiness Suggestions
- **PR → develop** is ready when: branch rebased; CI green; design link (or `needs-design-ref` + follow-up); complete PR body; Conventional Commit title; no blocking labels; changelog handled (RAT/manual).
- **Release PR (develop → main)** is ready when: meaningful changes since last tag; CI green on `develop`; release notes ready (RAT/manual); back-merge plan exists; no open P0/P1 for the scope; manual approval in GitHub.

## 23) Human + Machine Readability (Self-contained)
- Markdown with YAML front matter. Commit diagram sources (Mermaid/PlantUML/Graphviz). Avoid proprietary-only formats; provide text exports if necessary.
- Provide/update **`ai/manifest.json`** so tools find contract, design root, roadmap, KB root, labels, and versioning schemes.

### Changelog
- v2.0.0 — Remove `<BASE_BRANCH>`; standardize on **`develop`**. Tighten wording, clarify KB/wiki usage, and update tools/checklists to match.

