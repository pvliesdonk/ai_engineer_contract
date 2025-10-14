# Changelog

All notable changes to this project are documented here. Versions follow tags in `pvliesdonk/ai_engineer_contract`.
The project uses Conventional Commits and release-please.

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
