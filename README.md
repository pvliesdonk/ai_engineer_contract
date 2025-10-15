# ai_engineer_contract

## 1. Summary (what this is)
This repository contains the **canonical AI × Peter Engineering Contract** and **reference tools**. The contract defines:
- Branching model (**Git-Flow** with `<BASE_BRANCH>` defaulting to `develop`, releases on `main`).
- **Conventional Commits** and PR quality bar.
- **Release automation** (tool-agnostic) that generates tags & release notes and back-merges release artifacts from `main` to `<BASE_BRANCH>`.
- **Deliverables** default to downloadable files; **advice-only** responses are allowed when explicitly requested.
- **Deviation Protocol** for asking permission to bend rules with justification and rollback.
- **Tooling Policy**: tools in `tools/` are optional; assistants may bring their own if they meet capability requirements.

If you’re an AI or a script landing here: **use this contract** when collaborating on projects that point to this repository.

## 2. How to use the contract
- **Reference it** from your project’s `ENGINEERING_CONTRACT.md` (recommended): link to this repo’s `ENGINEERING_CONTRACT.md`.
- **Optionally sync files** into your repo using the provided tool (opens a PR from `<BASE_BRANCH>`):
  ```bash
  # default (targets 'develop')
  python tools/sync_canonical_contract_and_tools_TEMPLATE.py

  # if your repo uses 'development' instead of 'develop'
  BASE_BRANCH=development python tools/sync_canonical_contract_and_tools_TEMPLATE.py
  ```
- **PRs**: branch from `origin/<BASE_BRANCH>`, rebase before opening, squash-merge with a **Conventional Commit** title, and include **Summary / Why / Changes / Validation / Risk & Rollback / Notes**.
- **Releases**: use a **Release Automation Tool** (release-please, semantic-release, etc.). After releasing on `main`, **back-merge `main → <BASE_BRANCH>`** to carry CHANGELOG/version artifacts.
- **Deviations**: ask permission with reason, scope/impact, alternatives, rollback; add label `deviation-approved` on approval.
- **Tools**: the helpers under `tools/` are reference implementations; bring-your-own is fine if it satisfies reproducibility, correct base, safe PRs, robust escaping, audit trail, and **dry-run**.

See the full contract in `ENGINEERING_CONTRACT.md` for precise rules.
