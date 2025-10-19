# Changelog

All notable changes to this project are documented here. Versions follow tags in `pvliesdonk/ai_engineer_contract`.
The project uses Conventional Commits and release-please.


## [2.1.1](https://github.com/pvliesdonk/ai_engineer_contract/compare/a5cf015...ai_engineer_contract-v2.1.1) (2025-10-19)


### Documentation

* **contract:** codify release quality bar, SCM guidance, decision logging, and issue hygiene; require auto-creating missing labels ([#66](https://github.com/pvliesdonk/ai_engineer_contract/issues/66)) ([#65](https://github.com/pvliesdonk/ai_engineer_contract/issues/65)) ([bb27e60](https://github.com/pvliesdonk/ai_engineer_contract/commit/bb27e60bf9480b7073f597b3b6e92a9ab710b945)) ([3558552](https://github.com/pvliesdonk/ai_engineer_contract/commit/355855262c6e4396183b1615bf6b70069297c6ac)) ([81a1b22](https://github.com/pvliesdonk/ai_engineer_contract/commit/81a1b222de096889aa78fd3ca23554b672002b75))
* **contract:** add feedback/questions channel and remind PR authors to link issues ([969decd](https://github.com/pvliesdonk/ai_engineer_contract/commit/969decd5baff83d9d0286b6ffa5ab709593f96a7)) ([d1d46e9](https://github.com/pvliesdonk/ai_engineer_contract/commit/d1d46e9d2cdf6447fc0088dfb28ac4b7c7c2df7f))
* **kb:** document GitHub Projects integration and common CI fixes ([#64](https://github.com/pvliesdonk/ai_engineer_contract/issues/64)) ([6b1e4f8](https://github.com/pvliesdonk/ai_engineer_contract/commit/6b1e4f8b13b9ef0eb54de9cbeb4ad5e21d025ec1))
* **repo:** apply markdownlint auto-fixes across docs ([d94d84a](https://github.com/pvliesdonk/ai_engineer_contract/commit/d94d84a6a49333d60aa754db82728792cbdc4116))

### Continuous Integration

* add phase gate workflow driven by `phase.yaml` ([d6e72f5](https://github.com/pvliesdonk/ai_engineer_contract/commit/d6e72f5e77f82db532adc04d5150b958241ecb1f))


## [2.1.0](https://github.com/pvliesdonk/ai_engineer_contract/compare/ai_engineer_contract-v2.0.1...ai_engineer_contract-v2.1.0) (2025-10-16)


### Features

* **sync:** config-driven sync with provenance + docs ([#38](https://github.com/pvliesdonk/ai_engineer_contract/issues/38)) ([6e286c6](https://github.com/pvliesdonk/ai_engineer_contract/commit/6e286c6abd930c3a77dd7606f837ce8ef44d5fee))
* **tools:** implement sync_canonical_contract_and_tools_TEMPLATE.py with gh-based fetch, contract-only by default, optional template-tools sync; dry-run support\n\nFixes [#24](https://github.com/pvliesdonk/ai_engineer_contract/issues/24) ([#37](https://github.com/pvliesdonk/ai_engineer_contract/issues/37)) ([ea7821d](https://github.com/pvliesdonk/ai_engineer_contract/commit/ea7821d1cf5019ab12a513179252c6edb3ef46ed))

## [2.0.1](https://github.com/pvliesdonk/ai_engineer_contract/compare/ai_engineer_contract-v2.0.0...ai_engineer_contract-v2.0.1) (2025-10-16)

### Documentation

* clarify dual-role (contract host vs instance); add AI-driven CI tool selection guidance; KB intent + stubs; markdownlint reminders

### Miscellaneous Chores

* align manifest to release-please; add role=canonical-host; add example CI workflows

## [2.0.0](https://github.com/pvliesdonk/ai_engineer_contract/compare/ai_engineer_contract-v2.0.0-rc.1...ai_engineer_contract-v2.0.0) (2025-10-16)


### Miscellaneous Chores

* prepare GA ([#20](https://github.com/pvliesdonk/ai_engineer_contract/issues/20)) ([4da7b48](https://github.com/pvliesdonk/ai_engineer_contract/commit/4da7b48bcf712e1940ad502140ba2f3a08faa26b))

## [2.0.0-rc.1](https://github.com/pvliesdonk/ai_engineer_contract/compare/ai_engineer_contract-v1.6.4...ai_engineer_contract-v2.0.0-rc.1) (2025-10-16)


### Miscellaneous Chores

* prepare rc1 ([#13](https://github.com/pvliesdonk/ai_engineer_contract/issues/13)) ([986eba1](https://github.com/pvliesdonk/ai_engineer_contract/commit/986eba1a7466767ebe55b99ad29e37fe84a4af20))

## [1.6.4](https://github.com/pvliesdonk/ai_engineer_contract/compare/ai_engineer_contract-v1.6.0...ai_engineer_contract-v1.6.4) (2025-10-15)


### Features

* **tools:** add --base-branch and --dry-run; unify env knob; prep canonical/local handling for repo_bootstrap ([bdea11c](https://github.com/pvliesdonk/ai_engineer_contract/commit/bdea11cea55d288a82a15ce3c191902a0d90b340))
* **tools:** add --base-branch and --dry-run; unify env knob; prep canonical/local handling in pr_from_diff ([b8b0b1d](https://github.com/pvliesdonk/ai_engineer_contract/commit/b8b0b1decf93b9c0651b97c42939e8dd17e8b0a5))
* **tools:** add --base-branch and --dry-run; unify env knob; prep canonical/local handling sync_contract ([ca9fb02](https://github.com/pvliesdonk/ai_engineer_contract/commit/ca9fb02dc6990de6431a46d757a80971956cd5f4))


### Documentation

* **contract:** clarify back-merge rule and changelog ownership ([268e771](https://github.com/pvliesdonk/ai_engineer_contract/commit/268e7710a1f6b38fa91b61688cc4d7ebff069515))


### Miscellaneous Chores

* release ([0f7d570](https://github.com/pvliesdonk/ai_engineer_contract/commit/0f7d5703b4ff7f220fb0c379d077f36a8eaf9d97))

## [1.6.0](https://github.com/pvliesdonk/ai_engineer_contract/compare/ai_engineer_contract-v1.5.0...ai_engineer_contract-v1.6.0) (2025-10-14)


### Miscellaneous Chores

* updated changelog ([5c4e0b8](https://github.com/pvliesdonk/ai_engineer_contract/commit/5c4e0b89a2e29175045e615317d11b08681250b7))

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
