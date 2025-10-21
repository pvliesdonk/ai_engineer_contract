---
doc_type: kb_howto
doc_version: 2025-10-20.r1
title: Bind an AI to your repo's Engineering Contract
---

# Bind an AI to your repo's Engineering Contract

Use this copy‑paste prompt at the **start of a new chat** so the AI immediately follows the contract in your repository. Replace the repo URL as needed.

## Generic template

```text
You are bound by this repository’s Engineering Contract. Follow it immediately and without deviation.

Repo: https://github.com/<OWNER>/<REPO>
Primary sources:
- docs/design/ENGINEERING_CONTRACT.md
- AGENTS.md
- ai/manifest.json

Tasks:
1) Read those files.
2) Reply EXACTLY: ACK CONTRACT v2.3.0
3) Detect and state SCM mode (SCM-A / SCM-B / advise-only).
4) List the contract obligations you will follow here.
5) Propose 3 next steps.

Defaults (override if this repo says otherwise):
- Base branch develop; PRs → develop; squash merges.
- Plan issue before build; reference with “Fixes #ID”.
- Keep docs in sync (docs/design/**, docs/kb/**).
- Use label taxonomy from ai/manifest.json.
- Run pre-commit (markdownlint etc.); CI must pass.
- No secrets; use .env.example.
- Releases via release-please on main; back-merge main → develop.
- If advise-only, deliver ready-to-apply diffs and PR bodies.

Ask concise questions only if blocked. Acknowledge and proceed.
```

## Example for another repo

```text
You are bound by this repository’s Engineering Contract. Follow it immediately and without deviation.

Repo: https://github.com/pvliesdonk/planescape
Primary sources:
- docs/design/ENGINEERING_CONTRACT.md
- AGENTS.md
- ai/manifest.json

Do this now:
1) Fetch and read the above files.
2) Reply EXACTLY with: ACK CONTRACT v2.3.0
3) State SCM mode (SCM-A/SCM-B/advise-only) and proceed.
4) Summarize obligations you will follow.
5) Propose your first 3 concrete next steps.

Operational rules (confirm from repo):
- Base: develop; PRs → develop; squash.
- Plan before build; reference issue in PR (Fixes #123).
- Keep docs in sync; use standard labels; pass CI with pre-commit; no secrets; release-please main; back-merge main → develop.
```
