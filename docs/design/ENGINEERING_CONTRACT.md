# ENGINEERING_CONTRACT.md (AI × Peter) — v2.2.0

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

- **SCM-A — Full-Stack Agent:** direct access to code, `git`, `gh`, runtimes, and tokens. Do everything automatically (branches, commits, PRs, labels, issues, projects). Merge into **`develop`** after explicit chat approval. **Releases on `main` are always manual** (human presses the button). Allowed ops include pushing branches, running CI, creating repos/projects, and editing secrets (with approval).
- **SCM-B — IDE Co-Driver:** can edit files but cannot push. Provide ready-to-run scripts/patches and precise commands. Track readiness and tell the human when to merge or open release PRs. Allowed ops: local edits, diff generation, command suggestions, documentation updates. Disallowed: pushing, creating repos, mutating secrets.
- **SCM-C — Advise-Only Operator:** chat-only environment. Deliver structured guidance only—issue/PR bodies, review comments, checklists, and **optional inline unified diffs** for a single file. Use the templates in [`docs/kb/howtos/scm-c-advise.md`](../kb/howtos/scm-c-advise.md) so every hand-off stays copy/paste friendly.
  - **Deliverables:** Issue/plan/PR bodies, review summaries, validation or risk checklists, and single-file inline unified diffs wrapped in fenced code blocks with application notes.
  - **Forbidden:** Filesystem edits, git commands, running scripts, archive/patch uploads, or automated PR/branch creation.
  - **Escalate:** When the requested change spans multiple files, requires command execution or automation, or the human asks for direct code edits beyond the documented inline diff scope.
- Detect mode once per session following this flow:
  1. **Auto-detect** capabilities (check git push access, filesystem access, `gh` auth). If unclear, ask the human to confirm the mode.
  2. **Confirm** before performing privileged actions (creating repos, changing default branches, toggling visibility).
  3. **Log** any mode switch in the conversation and in the PR body if it impacts work.
- Use the decision tree in `docs/kb/howtos/scm-mode-decision-tree.md` before running operations that require elevated access (e.g., `gh repo create`, secret updates).

### SCM deliverables & escalation

| Mode  | Primary outputs                                                                 | Escalate when…                                               |
| ----- | -------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| SCM-A | Branches, commits, PRs, CI runs, repo/label automation                           | Human approval required for privileged ops (secrets, repos). |
| SCM-B | Local edits, diffs/patches, scripts, documentation updates                      | Work needs direct pushes, multi-repo automation, or secrets. |
| SCM-C | Advise-only packages via docs/kb/howtos/scm-c-advise.md templates (issues, reviews, checklists, inline diffs) | Task requires multi-file edits, command execution, automation, or non-templated assets. |

### Agent Operating Guardrails

- Always restate the detected SCM mode and base branch (`develop`) before taking privileged actions. If the environment changes mid-session, pause and re-confirm with a human.
- Operate behind a referenced Plan issue (unless `plan-exempt` is explicitly granted) and branch from `origin/develop` using the contract naming scheme. Document the plan with acceptance criteria and validation before editing docs/config/code.
- Apply the required PR labels: `from-ai`, `needs-review`, and an appropriate scope label (`docs`, `chore`, etc.). Auto-create missing labels with `gh label create`.
- Post a “Proposed solution” comment on the tracked issue before implementation. Keep it up to date as work evolves and link to the eventual PR.
- Enforce secrets hygiene: never store or echo tokens, redact sensitive output, and request escalated permissions only when unavoidable. Decline work that would expose secrets or violate org policy.
- If instructions conflict, would bypass `phase.yaml`, or exceed the current CI/approval guardrails, escalate via a `feedback` issue instead of proceeding. Document any deviations with `deviation-approved` and explicit rollback steps.

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
- Follow the feedback pipeline:
  - `feedback` issues capture raw input and MAY close without action.
  - Elevate accepted ideas into `feature proposal` issues to explore scope and validation.
  - Promote vetted proposals into `design change` issues when design docs are ready to update. Cross-link each hop so history stays auditable.

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

### Pre-Build Allowed Work

- **Allowed:** Documentation authoring (requirements, architecture, roadmap, KB), repository administration (labels, milestones, Projects), issue triage, decision logging, and contract-aligned planning artifacts.
- **Disallowed:** Creating/modifying source code, tests, generated assets, or build/CI scripts; setting up scaffolding that belongs in the implementation phase; introducing binaries or vendored content.
- **Pro tip:** Anything that changes runtime behavior belongs behind a tracked Plan issue before editing code/tests/config/docs.
- Before leaving the planning phase, open or update a Plan issue (`.github/ISSUE_TEMPLATE/plan.yml`) that captures acceptance criteria and validation. Reference that issue in subsequent PRs (`Fixes #ID`). Use the `plan-exempt` label only for maintainer-approved micro-fixes and document the rationale.
- Add this checklist to any PR that lands before implementation work begins (all boxes must be ✅):

```text
- [ ] Only docs/planning/ops work (no code/tests/assets)
- [ ] Plan issue (#ID) drafted/updated with acceptance criteria & validation
- [ ] Linked requirements/design docs updated
- [ ] Decisions captured in docs/design/DECISIONS.md (and YAML if used)
```

### Decision Elicitation Protocol & Logging

- Ask **one decision at a time**, presenting 1–3 options and clearly marking the recommended default.
- Confirm the choice, rationale, and owner, then log the outcome in `docs/design/DECISIONS.md`.
- Optionally create machine-readable entries in `docs/design/decisions/*.yaml` mirroring the log table.
- Reference decision IDs from issues/PRs and keep the log in sync with design updates and approvals.

### Model Recommendations in Plans

- Planning artifacts MAY recommend **model families** for AI-assisted work. Prefer the organization’s approved model catalog and reference the latest generally available versions.
- When no org policy exists, name the family (e.g., “OpenAI GPT-5”, “OpenAI GPT-4.1”) and provide a short rationale with acceptable fallbacks that cover cost, latency, and privacy constraints.
- Record recommendations in docs; pin exact SKUs only in deployable configuration files. Revisit the recommendations at each release or when upstream models change materially.
- Use the provider matrix and task routes published in `docs/kb/howtos/model-recommendations.md`. At minimum, capture the shared provider families so downstream repos stay aligned:

```yaml
ai_assist:
  providers:
    openai:
      primary: gpt-5
      thinking: gpt-5-thinking
      fast: o4-mini
      long_context: gpt-4.1
    google:
      primary: gemini-2.5-flash
      thinking: gemini-2.5-pro
      fast: gemini-2.5-flash-lite
      long_context: gemini-2.5-pro
    ollama:
      primary: llama3.1:8b-instruct-q4_K_M
      thinking: deepseek-r1:7b
      fast: mistral:7b-instruct
      long_context: mistral:7b-instruct
  notes: >
    Document families in planning; pin exact SKUs only in deployable config.
    For local models on 8 GB GPUs, prefer Q4_K_M quantizations for stability.
```

- Route guidance covers common tasks (`scm_c_advise`, `policy_edit`, `bulk_scaffold`, `long_context`, `bulk_narration`, `bulk_programming`) across OpenAI, Google AI Studio, and local Ollama options so maintainers can tailor usage per scenario.

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
- Encode AI assistance defaults in the manifest. Mirror the provider families/routes from `docs/kb/howtos/model-recommendations.md` so automation can reason about tasks:

```json
{
  "ai_assist": {
    "providers": {
      "openai": { "primary": "gpt-5", "thinking": "gpt-5-thinking", "fast": "o4-mini", "long_context": "gpt-4.1" },
      "google": { "primary": "gemini-2.5-flash", "thinking": "gemini-2.5-pro", "fast": "gemini-2.5-flash-lite", "long_context": "gemini-2.5-pro" },
      "ollama": { "primary": "llama3.1:8b-instruct-q4_K_M", "thinking": "deepseek-r1:7b", "fast": "mistral:7b-instruct", "long_context": "mistral:7b-instruct" }
    },
    "review_on_release": true
  }
}
```

### Changelog

- v2.2.0 — Enforce Plan → Build gating, issue template, workflow guardrails, and release automation token check.
- v2.1.2 — Guard contract version references and document release checklist; align release manifest updates.
- v2.1.1 — Document quality bar expectations, decision logging, and issue hygiene; add feedback channel, PR linked-issue reminder, and SCM phase gate workflow.
- v2.0.2 — Clarify dual-role hosting vs instance; add AI CI tool selection guidance; add minimal contract capsule and binding prompt.
- v2.0.1 — Add pre-implementation discipline, milestone branch guidance, and early CI setup recommendation.
- v2.0.0 — Remove `<BASE_BRANCH>`; standardize on **`develop`**. Tighten wording, clarify KB/wiki usage, and update tools/checklists to match.

## 24) AGENTS.md Convention

- Add an `AGENTS.md` at the repository root to define agent behavior for this codebase.
- Scope and precedence:
  - A root `AGENTS.md` applies to the entire repository tree.
  - A nested `AGENTS.md` applies to its subtree and overrides rules from higher levels when in conflict.
  - Direct instructions from a human (issue/PR/chat) take precedence over `AGENTS.md` files.
- **Mandatory sections** (use these headings verbatim):
  - `## Contract Link & Scope`
  - `## Planning Sources`
  - `## Plan & Build Gate`
  - `## Branching, PRs & Labels`
  - `## CI & Tooling`
  - `## Security & Secrets`
  - `## Session Modes (SCM-A/B/C)`
- Each section must describe: base branch (`develop`), PR/merge rules (squash into `develop`), Conventional Commit titles, release automation, documentation roots (`docs/design`, `docs/kb`), required labels, CI expectations, secrets handling, and how to escalate/confirm SCM modes.
- Keep `AGENTS.md` short, actionable, and consistent with this contract. Link to `docs/design/ENGINEERING_CONTRACT.md` for details.
- Provide the following snippet (update repository-specific details only):

````markdown
# AGENTS.md — AI Agent Instructions (repo-wide)

## Contract Link & Scope
- Authoritative contract: [docs/design/ENGINEERING_CONTRACT.md](docs/design/ENGINEERING_CONTRACT.md)
- Base branch: `develop`; PRs target `develop`; releases via release-please on `main`.

## Planning Sources
- Requirements/design live in `docs/design/`; knowledge base in `docs/kb/`.
- Keep `docs/design/requirements.md`, `architecture.md`, `DECISIONS.md`, and ADRs current before coding.

## Plan & Build Gate
- Build work requires a referenced Plan issue (`Fixes #ID` / `Refs #ID`) unless the PR carries `plan-exempt`.
- Pre-build PRs follow the contract checklist; focus on docs/planning/ops only.
- Update the Plan issue when scope or acceptance criteria change.

## Branching, PRs & Labels
- Branch naming: `feat|fix|docs|chore|refactor|test/<slug>`.
- Rebase on `origin/develop`; squash-merge after approval.
- Apply `from-ai`, `needs-review`, plus scope labels (`docs`, `chore`, etc.) as appropriate.

## CI & Tooling
- Run markdownlint for docs-only changes; follow contract guidance for additional stacks.
- Keep `ai/manifest.json` and CI workflows in sync with repo capabilities. release-please runs automatically on `main`; use workflow dispatch for manual retries if needed.

## Security & Secrets
- Never commit secrets; use `.env.example`.
- Redact tokens in logs/PRs; coordinate with maintainers for secret rotation.

## Session Modes (SCM-A/B/C)
- Detect mode once per session; confirm capabilities with the human if unclear.
- SCM-A may push/PR (merge only with approval); SCM-B offers instructions; SCM-C delivers advise-only packages using `docs/kb/howtos/scm-c-advise.md` (no archives or direct file edits).
````

## 26) CI Phase Gates

- Enforce the repository phase using a root `phase.yaml` and CI path allowlists.
  - `phase: requirements|design|plan|build`
  - Optional `allowed_paths:` overrides default allowlists per phase.
- Defaults:
  - requirements/design: `docs/**`, `AGENTS.md`, `ai/**`, `phase.yaml`
  - plan: above + `.github/**`
  - build: unrestricted
- Maintain `.github/workflows/phase-gate.yml` (or equivalent) so every PR runs the phase gate against `phase.yaml`. The workflow MUST fail fast when a change touches disallowed paths.
- Temporary deviation: add the `deviation-approved` label and include rationale and rollback in the PR body.
- Advancing the phase is an auditable one-file change: update `phase.yaml` in a separate PR.

## 27) Quality Bar Enforcement

- Maintain a Quality Bar linter that checks:
  - Front matter title matches first H1.
  - Required status fields are present.
  - No placeholder-only sections remain (e.g., bare “TODO” headings).
  - Document links resolve (use a link checker).
  - Citations include identifiers and page spans when quoting physical sources.
- Adoption cadence:
  1. Wire the linter locally; run in `warn-only` mode in CI during requirements/design phases.
  2. Promote to blocking once the repository reaches `phase: build`.
- Run `.github/workflows/docs-quality.yml` (or equivalent) on docs-affecting PRs. Include at minimum `markdownlint-cli2` and a link checker such as `lychee` configured to fail on errors and surface actionable logs.
- Document the chosen implementation (Python/Node) and share remediation guidance in CI output.
- Reference: `docs/kb/howtos/quality-bar-linter.md`.

## 28) IP Rights & Attestation

- Every repository MUST include an `IP_DISCLAIMER.md` (or equivalent) with the rights attestation template from `docs/kb/howtos/ip-disclaimer.md`.
- Contributors must state whether extended quotations are allowed and under which licence/terms.
- Citations require source identifiers:
  - Physical media: include page spans (e.g., “pp. 12–15”).
  - Online sources: include permalink + retrieval date.
- Catalog third-party assets with licence metadata and attribution text.
- Escalate novel IP questions to the policy contact listed in the disclaimer before merging.

## 29) Dual-Role Transparency

- Distinguish canonical vs instance assets as described in `docs/kb/dual-role.md`.
- Annotate instance-only workflows and automation with header comments clarifying scope.
- Keep canonical templates (`tools/*_TEMPLATE.py`, design templates) free of repository-specific defaults; place instance-specific automation under `tools/local/` or equivalent.
- Update the README and knowledge base when new instance-specific workflows or scripts are introduced.
