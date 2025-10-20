---
doc_type: kb_howto
doc_version: 2025-10-20.r1
title: Getting Started — Using the AI Engineer Contract
---

# Getting Started

This guide helps contributors and consumers start quickly while staying inside the contract.

## 1) Clone & Branch

```bash
# clone your fork or the repo
# ensure you branch from develop

git checkout -b docs/first-change origin/develop
```

## 2) Install hooks (optional, recommended)

```bash
# Run pre-commit locally to catch common issues
pipx install pre-commit || python -m pip install --user pre-commit
pre-commit install --install-hooks
pre-commit run --all-files
```

## 3) Initialize labels (once per repo)

```bash
python tools/ai_contract_cli.py labels init
```

## 4) Plan before build

Open a small Plan issue describing what you’ll change and why. Link your PR with `Fixes #<id>`.

## 5) Open a PR to `develop`

- Use the PR template.
- Keep PRs small; squash-merge.
- For docs-only or config-only edits, CI should pass with lint + byte-compile.

## 6) Advise-only mode

When you don’t have write access, deliver **advise-only** packages (formerly “SCM-C”): issues, PR bodies, review diffs. See [Advise‑Only Templates](advise-only-templates.md).

## 7) Sync the canonical contract (for downstream repos)

```bash
# bring the latest contract (and optionally tools) into your repo
python tools/sync_canonical_contract_and_tools_TEMPLATE.py --include-tools
```

## 8) Release docs site

This repo’s `main` branch publishes a MkDocs site via GitHub Pages. Enable Pages for the `gh-pages` branch in repo settings.

**Related how‑tos:**
- [Phase Gates](phase-gates.md)
- [Model Recommendations](model-recommendations.md)
- [Advise‑Only Templates](advise-only-templates.md)
