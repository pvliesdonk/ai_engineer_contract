# ENGINEERING_CONTRACT.md (AI x Peter) - v1.4.0
Effective: 2025-10-14 11:36:09 UTC
Owner: Peter van Liesdonk (pvliesdonk)
Purpose: Consistent, auditable collaboration on software and docs.

This is the canonical contract. Keep a copy at the repository root and reflect it in the ChatGPT Project prompt.

---
1) Branches & Flow
- Work under pvliesdonk/{repo_name}.
- main = releases only (via develop -> main when requested).
- develop = base for PRs. Use feat/<slug>, fix/<slug>, docs/<slug>, chore/<slug>, refactor/<slug>, test/<slug>.
- Always rebase on origin/develop before PR. Squash-merge into develop.

2) PR Quality
- Conventional Commit title (feat:, fix:, ...).
- Body: Summary, Why, Changes, Validation, Risk & Rollback, Notes.
- Small, focused diffs; update docs/tests with behavior changes.

3) Releases
- PR develop -> main titled release: vX.Y.Z. After merge, tag vX.Y.Z and create a GitHub Release.

4) Access Modes
- With GitHub access: operate directly under this contract.
- Without access: deliver a single-file PR script using git + gh that branches from origin/develop, applies embedded changes, creates missing labels, and opens a PR to develop.

5) Artifact Delivery - ALWAYS Downloadable (UPDATED)
- Every deliverable (scripts, long diffs, docs) must be provided as a downloadable file in chat.
  Short scripts may also be shown inline; long ones can be hidden but still downloadable.
- Provide a one-paragraph synopsis and exact run command(s) for each artifact.

6) Robust Delimiters & Escaping
- Use raw triple-quoted strings (r"""..."""), normalize to LF, base64 for binary/fragile payloads, and single-quoted heredocs (<<'EOF'). Optional SHA-256 verification for payloads.

7) Security
- No secrets. Use .env.example, .gitignore. Redact sensitive values in logs/PRs.

8) Communication
- Concise progress; deterministic scripts; pin versions where sensible.

9) Non-Programming Repos
- Same process. Validation adapts (link checkers, Markdownlint, MkDocs/mdBook, etc.).

10) New Repo Bootstrap
- Confirm LICENSE first (default MIT). Create LICENSE, README.md, CONTRIBUTING.md, minimal .gitignore. Create/push main and develop. Ensure default labels exist.

11) Canonical Source & Distribution
- Canonical repo: pvliesdonk/ai_engineer_contract.
- Every new repo must include the latest ENGINEERING_CONTRACT.md and the tools/ folder:
  - tools/pr_from_diff_TEMPLATE.py
  - tools/repo_bootstrap_TEMPLATE.py
- Acceptable mechanisms: copy at creation, template repo, or git subtree for tools/ (avoid submodules unless strictly needed).

12) Labels
- Commits/PRs must include appropriate labels. Scripts auto-create missing labels via gh label create.

13) Auto-Upgrade in Chat (NEW)
- When a newer contract version or tool appears within the current chat/project, the AI must immediately switch to the newest available version for subsequent actions in this conversation.

14) Auto-Update Repositories (NEW)
- When a newer contract or tool is available in chat, the AI must also update the active repository to that version by opening a PR that replaces ENGINEERING_CONTRACT.md and tools/* with the newer versions (unless the user opts out).
- PR title: chore: sync canonical contract/tools to v<version>. Labels: from-ai, needs-review, docs.
- If local deltas exist, call them out in the PR body; prefer preserving project-specific sections in ENGINEERING_CONTRACT_LOCAL.md.

---
Cheatsheet
- git fetch --all --prune
- git checkout develop && git reset --hard origin/develop
- git switch -c feat/<slug>
- git add -A && git commit -m "feat: <title>"
- git push -u origin HEAD
- gh pr create --base develop --title "feat: <title>" --body-file pr.md --label from-ai --label needs-review

Suggested Labels (auto-created if absent)
from-ai, needs-review, blocked, security, breaking-change, docs, chore, content, design, asset

---
Changelog
- v1.4.0 - Always provide deliverables as downloads; auto-switch in chat; auto-update repos.
- v1.3.0 - Canonical distribution across repos.
- v1.2.0 - New repo bootstrap (license confirmation, CONTRIBUTING).
- v1.1.0 - Robust escaping, auto-labels, non-code repos.
- v1.0.1 - Scripts downloadable; inline for short ones.
- v1.0.0 - Initial.
