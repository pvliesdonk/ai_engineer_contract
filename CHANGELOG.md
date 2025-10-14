# Changelog

All notable changes to this project are documented here. Versions follow tags in `pvliesdonk/ai_engineer_contract`.
The project uses Conventional Commits and release-please.



## [1.6.0] - Advice-only + Commit Proposals
### Documentation
- Add advice-only mode: when the user asks specifically for advice, return guidance/snippets without packaging deliverables.
- Require the AI to propose 1–3 Conventional Commit messages after each deliverable.

## [1.5.0] - Branch defaults + TODO stubs
### Documentation
- Keep `develop` as the default base branch; allow `BASE_BRANCH=development` override.
- Require explicit TODO markers and `NotImplemented`-style failures for stubs.
### Features
- `pr_from_diff_TEMPLATE.py` v1.1.1: support `BASE_BRANCH` env override.
### Chore
- `repo_bootstrap_TEMPLATE.py` v1.2.1: add `DEV_BRANCH` env override.
- Add release-please configuration and workflow.

## [1.4.1] - Alias of 1.4.0
### Documentation
- Rename/organize without semantic change.

## [1.4.0] - Download-by-default + Auto-upgrade + Sync
### Documentation
- Always provide deliverables as downloads.
- Auto-upgrade to the latest contract/tool in the current chat.
- Auto-PR to sync repositories with the latest contract and tools.
### Features
- Add `sync_canonical_contract_and_tools_TEMPLATE.py` v1.1.0.

## [1.3.0] - Canonical distribution
### Documentation
- Define canonical repository and distribution rules for contract + tools.
### Features
- Add `pr_from_diff_TEMPLATE.py` v1.1.0.
### Chore
- Move helper scripts into `tools/` directory.

## [1.2.0] - Bootstrap
### Documentation
- Add repository bootstrap steps (license, CONTRIBUTING, labels).
### Features
- Add `repo_bootstrap_TEMPLATE.py` v1.2.0.

## [1.1.0]
### Documentation
- Robust escaping and label auto-create across repos; non-programming repos follow the same review flow.

## [1.0.1]
### Documentation
- Deliverables must be downloadable; allow inline display for short scripts.

## [1.0.0]
### Documentation
- Initial canonical contract and minimal README.
