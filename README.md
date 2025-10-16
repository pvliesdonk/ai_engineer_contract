# ai_engineer_contract

## 1) Summary
This repository hosts the **canonical AI × Peter Engineering Contract** and reference tools. The contract standardizes:
- Branching (Git-Flow with `<BASE_BRANCH>` = `develop` by default; releases on `main`).
- **Conventional Commits** and PR quality.
- **Release automation** (tool-agnostic) with a back-merge from `main → <BASE_BRANCH>`.
- **Deliverables** are downloadable by default; **advice-only** is allowed when explicitly requested.
- **Deviation Protocol** for exceptions (ask permission with justification & rollback).
- **Tooling Policy** (optional; bring-your-own allowed if it meets capability requirements).
- **Requirements & Design Phase** before building, with docs in `docs/design/`.
- **Issue & Project Management**: the AI can create issues/labels/milestones/projects and must reference design docs.

👉 Any AI or script landing here should **apply this contract** when a project points to it.

## 2) How to use the contract
- **In your project repo:**
  - Keep a copy at **`docs/design/ENGINEERING_CONTRACT.md`** linking back to the canonical version here.
  - Maintain design docs in `docs/design/` (`requirements.md`, `architecture.md`, ADRs).
- **Optionally sync** latest contract/tools via the helper (opens a PR against `<BASE_BRANCH>`):
  ```bash
  # default (targets 'develop')
  python tools/sync_canonical_contract_and_tools_TEMPLATE.py

  # if your repo uses 'development' instead of 'develop'
  BASE_BRANCH=development python tools/sync_canonical_contract_and_tools_TEMPLATE.py
  ```
- **Open work as issues** linked to design sections/ADRs; group with labels, milestones, and a Project.
- **PRs**: branch from `origin/<BASE_BRANCH>`, rebase before opening, squash-merge with a Conventional Commit title, and include **Summary / Why / Changes / Validation / Risk & Rollback / Notes**.
- **Releases**: use a Release Automation Tool (e.g., release-please, semantic-release). After merging the release PR to `main`, back-merge into `<BASE_BRANCH>`.

See the full contract in `ENGINEERING_CONTRACT.md` for authoritative details.
