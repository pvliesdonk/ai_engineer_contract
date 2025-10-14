# Changelog

All notable changes to this project are documented here. Versions follow tags in `pvliesdonk/ai_engineer_contract`.
The project uses Conventional Commits and release-please.


## [1.5.0](https://github.com/pvliesdonk/ai_engineer_contract/compare/ai_engineer_contract-v1.2.0...ai_engineer_contract-v1.5.0) (2025-10-14)


### Features

* **tools:** add pr_from_diff_TEMPLATE.py v1.1.0 ([c4f30c3](https://github.com/pvliesdonk/ai_engineer_contract/commit/c4f30c33cac56b32eea463a1d2bd3827ded5f087))
* **tools:** add sync_canonical_contract_and_tools_TEMPLATE.py v1.1.0 ([c4f30c3](https://github.com/pvliesdonk/ai_engineer_contract/commit/c4f30c33cac56b32eea463a1d2bd3827ded5f087))
* **tools:** pr_from_diff_TEMPLATE.py v1.1.1 — support BASE_BRANCH env override ([67f4980](https://github.com/pvliesdonk/ai_engineer_contract/commit/67f4980c006fb24c7b5ef0d29e3939967d24c464))


### Documentation

* **contract:** enforce always-download; auto-upgrade in chat; repo sync PRs ([c4f30c3](https://github.com/pvliesdonk/ai_engineer_contract/commit/c4f30c33cac56b32eea463a1d2bd3827ded5f087))
* **contract:** rename/organize without semantic changes ([8faeb95](https://github.com/pvliesdonk/ai_engineer_contract/commit/8faeb955877fbca30a798271954e5ad7a0e50222))
* **contract:** set develop as default; add BASE_BRANCH override; require TODO stubs ([67f4980](https://github.com/pvliesdonk/ai_engineer_contract/commit/67f4980c006fb24c7b5ef0d29e3939967d24c464))

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
