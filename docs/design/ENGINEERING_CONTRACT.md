# ENGINEERING_CONTRACT.md (AI × Peter) — v2.0.2

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

### Issue Hygiene & Proposal Tracking

- Always open issues for next steps and discrete work items; link related design/KB sections.
- When picking up an issue, add a top comment titled “Proposed solution” that summarizes:
  - Scope and approach, validation/acceptance criteria, risks/rollback, and labels.
  - Any contract/process implications (e.g., phase vs harness alignment) and planned CI checks.
- Keep the comment updated if the approach changes; link the PR and reference the comment in the PR body.
- Use labels from the taxonomy (e.g., `from-ai`, `needs-review`, `docs`, `chore`).

### Feedback & Questions

- AIs and consumers SHOULD open issues on the canonical repository for ambiguities, questions, or improvement proposals.
- Use labels: `feedback` and `question` (and others as appropriate).
- Include concrete references (file path + heading) and a minimal reproduction or example PR where helpful.

## 9) Programming-Adjacent Projects (Docs/KBase/Wiki)

- The same PR/review flow applies. Validation adapts (link checkers, Markdownlint, doc build if any).
- **Docs live under `docs/`**. For knowledge bases, prefer **`docs/kb/`** with an **`index.md`** (front matter + TOC).
- Design docs (requirements/architecture/ADRs) live under **`docs/design/`**.
- **Versioning separation:** Releases use **SemVer**; design/kb docs use **date+revision** (`doc_version: YYYY-MM-DD.rN` in YAML front matter).
- Issues/PRs must link to the relevant doc sections; the AI may create issues/labels/milestones/projects.

## 10) New Repo Bootstrap

- Confirm LICENSE (usually **MIT**). Create `LICENSE`, `README.md`, `CONTRIBUTING.md`, minimal `.gitignore`. Create/push `main` and `develop`. Ensure default labels exist.
- Set up minimal CI immediately (e.g., markdown lint, script byte-compile, basic format/type checks) so the very first commits are validated.
- AI selects CI tools based on the stack being introduced. At minimum include lint/format checks and a smoke run where applicable.

## 11) Canonical Source & Distribution

- Canonical repo: `pvliesdonk/ai_engineer_contract`. Keep the contract in consumer projects at `docs/design/ENGINEERING_CONTRACT.md` with a link back here.
- Include the latest contract and (optionally) `tools/` in new repos. You may sync updates via PR.
- Include a root `AGENTS.md` that summarizes how AI agents should operate in the repo (see section 24).
- Dual role note: This repository both hosts the generic, tool-agnostic contract and implements it for itself. Consumers should follow the contract text; workflows here (e.g., release-please) are examples, not mandates.

## 12) Labels

- Commits/PRs should have labels. Agents SHALL auto-create missing labels at PR time.
- Scripts SHOULD create missing labels via `gh label create` (idempotent) and MAY add repo-specific labels like `ci`, `feedback`.
- Suggested labels: `from-ai`, `needs-review`, `docs`, `chore`, `security`, `blocked`, `planning`, `needs-design-ref`, `breaking-change`, `content`, `design`, `asset`, `deviation-approved`, `feedback`.

Example (idempotent) label creation

```bash
gh label create from-ai --color 5319e7 --description "Auto-created label - from-ai" --force
gh label create needs-review --color d93f0b --description "Auto-created label - needs-review" --force
gh label create ci --color 5319e7 --description "Auto-created label - ci" --force
gh label create feedback --color 1d76db --description "Feedback and questions" --force
```

## 13) Auto-Upgrade in Chat & Repos

- When a newer contract/tool appears in the current chat, immediately use it.
- Open a PR to update `ENGINEERING_CONTRACT.md` and **replace only canonical** `tools/canonical/*` if you’re using them; keep `tools/local/*` intact.

## 14) TODOs & Not-Implemented Stubs

- Stubbed code must include explicit TODO markers and fail fast (language-appropriate `NotImplemented`/exceptions or warnings). Place TODOs at call sites and function bodies.

## 15) Conventional Commit Proposals

- After every deliverable, propose 1–3 candidate Conventional Commit messages and a PR title.

## 16) Changelog & Release Notes

- The **RAT** is the source of truth for release notes and `CHANGELOG.md` (if enabled). Don’t edit generated changelog entries by hand. If no RAT, PRs must update `CHANGELOG.md`.
- Documentation as a core deliverable (SemVer semantics): when documentation is part of the shipped product (e.g., this contract), use Conventional Commits to drive SemVer:
  - Breaking normative change: `docs(contract)!: …` and include a `BREAKING CHANGE:` footer; release = MAJOR.
  - New normative capability/allowance: `feat(contract): …`; release = MINOR.
  - Clarification or non-normative bug fix: `fix(contract): …`; release = PATCH.
  - Editorial/formatting only: `docs(contract): …` (may not trigger a release). If you need a tag, add a `Release-As: x.y.z` footer.
  - Note: Some release tools hide `docs:` by default and do not bump versions for it. Prefer `feat:`/`fix:` when the change is normative and should bump.

## 17) Deviation Protocol

- Request permission to deviate: include reason, scope/impact, alternatives, rollback. Approval by **Peter** or a **CODEOWNER**. Label `deviation-approved`; document in the PR and changelog if user-visible.

## 18) Requirements & Design Phase

- Before building, perform requirements + design and commit docs to `docs/design/`:
  - `requirements.md`, `architecture.md`, `decision-log/ADR-YYYYMMDD-<slug>.md`
  - Optional: `test-plan.md`, `roadmap.md`, diagrams (commit sources).
- Update docs with each PR that changes behavior/scope.
- Never eagerly start programming. Complete requirements and design first and get explicit go-ahead before implementation.

## 19) Issue & Project Management (AI allowed)

- The AI may create issues/labels/milestones/projects. **Design-impacting work must link to design docs**, otherwise label `needs-design-ref` and add the doc before implementation.
- Link PRs to issues (`Fixes #123`). Avoid assigning people unless asked; prefer milestones/projects.

## 20) Planning vs Releases

- Plan by **Milestones** (`M1`, `M2`, …) and optional **Release Trains** (`RYYYY.MM`, `RYYYYQn`), not by future SemVer.
- Record the *actual* shipped tags **after** release in `docs/design/delivery-map.yml`.
- Develop milestones on dedicated branches. Pull issues into the milestone branch via PRs. Avoid parallel work on potentially conflicting issues; if multiple issues converge on the same milestone, chain branches (base follow-up branches on the predecessor) to minimize conflict.

## 21) Branching Discipline

- All work happens on a topic branch off `origin/develop` (`feat/<slug>`, `fix/<slug>`, etc.).
- Keep **many small commits**. Squash-merge into `develop`.
- Keep branches **rebased** on `origin/develop`. Do **not** delete topic branches until the change is released and back-merged (`main` → `develop`).
- Prefer serializing changes that touch the same codepaths to reduce merge conflicts. When concurrency is required, coordinate base branches to create a linear chain.

## 25) CI Tool Selection Guidance (AI)

- The AI chooses minimal CI appropriate to the stack introduced by the change. Examples (non-exhaustive):
  - Python: ruff/flake8, black (or equivalent formatter) in check mode, `python -m py_compile tools/*.py`, and `pytest -q` smoke if tests exist.
  - Node/TypeScript: eslint, prettier check, `tsc --noEmit` if TypeScript, and `npm test -s` smoke where present.
  - Shell: shellcheck.
  - Docs-only: markdownlint.
  - Go: golangci-lint, `go test ./...`.
  - Rust: `cargo fmt -- --check`, `cargo clippy -- -D warnings`, `cargo test`.
  - Terraform: `terraform fmt -check`, `terraform validate` (with init).
  - Dockerfiles: hadolint.
- Integrate CI as early as possible (bootstrap or first meaningful PR). Keep checks fast and additive over time.

## 22) Merge-Readiness Suggestions

- **PR → develop** is ready when: branch rebased; CI green; design link (or `needs-design-ref` + follow-up); complete PR body; Conventional Commit title; no blocking labels; changelog handled (RAT/manual).
- **Release PR (develop → main)** is ready when: meaningful changes since last tag; CI green on `develop`; release notes ready (RAT/manual); back-merge plan exists; no open P0/P1 for the scope; manual approval in GitHub.

## 23) Human + Machine Readability (Self-contained)

- Markdown with YAML front matter. Commit diagram sources (Mermaid/PlantUML/Graphviz). Avoid proprietary-only formats; provide text exports if necessary.
- Provide/update **`ai/manifest.json`** so tools find contract, design root, roadmap, KB root, labels, and versioning schemes.

### Changelog

- v2.0.2 — Clarify dual-role hosting vs instance; add AI CI tool selection guidance; add minimal contract capsule and binding prompt.
- v2.0.1 — Add pre-implementation discipline, milestone branch guidance, and early CI setup recommendation.
- v2.0.0 — Remove `<BASE_BRANCH>`; standardize on **`develop`**. Tighten wording, clarify KB/wiki usage, and update tools/checklists to match.

## 24) AGENTS.md Convention

- Add an `AGENTS.md` at the repository root to define agent behavior for this codebase.
- Scope and precedence:
  - A root `AGENTS.md` applies to the entire repository tree.
  - A nested `AGENTS.md` applies to its subtree and overrides rules from higher levels when in conflict.
  - Direct instructions from a human (issue/PR/chat) take precedence over `AGENTS.md` files.
- Content should cover: base branch (`develop`), PR/merge rules, Conventional Commits, release process (`develop → main` via release automation + backmerge), docs locations (`docs/design`, `docs/kb`), labels, CI expectations, and security/secrets policy.
- Keep `AGENTS.md` short, actionable, and consistent with this contract. Link to `docs/design/ENGINEERING_CONTRACT.md` for details.

## 26) CI Phase Gates

- Enforce the repository phase using a root `phase.yaml` and CI path allowlists.
  - `phase: requirements|design|plan|build`
  - Optional `allowed_paths:` overrides default allowlists per phase.
- Defaults:
  - requirements/design: `docs/**`, `AGENTS.md`, `ai/**`, `phase.yaml`
  - plan: above + `.github/**`
  - build: unrestricted
- CI fails PRs that touch disallowed paths for the current phase.
- Temporary deviation: add the `deviation-approved` label and include rationale and rollback in the PR body.
- Advancing the phase is an auditable one-file change: update `phase.yaml` in a separate PR.
