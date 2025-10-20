---
doc_type: kb_howto
doc_version: 2025-10-20.r1
title: Repo hygiene with pre-commit (contract-friendly)
---

# Repo hygiene with pre-commit (contract‑friendly)

This how‑to gives a **minimal, tool‑agnostic** setup that matches the contract’s guidance. It keeps diffs clean and CI fast without forcing a language stack.

## Why this setup

- Catch nits early (whitespace, EOF, YAML/JSON)
- Keep Markdown readable (markdownlint)
- Enforce commit message shape (gitlint)
- Same checks locally and in CI

## 1) Add the config

Create `.pre-commit-config.yaml` at the repo root (or extend your existing one):

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict
      - id: mixed-line-ending
      - id: check-yaml
      - id: check-json
  - repo: https://github.com/jorisroovers/gitlint
    rev: v0.19.1
    hooks:
      - id: gitlint
        stages: [commit-msg]
  - repo: https://github.com/DavidAnson/markdownlint-cli2
    rev: v0.15.0
    hooks:
      - id: markdownlint-cli2
        args: ["--fix"]
```

Optional: customize rules with `.markdownlint-cli2.yaml` (kept tiny):

```yaml
# .markdownlint-cli2.yaml
config:
  MD013: false   # no max line length for prose
```

## 2) Install and run locally

Use any Python—this stays **stdlib + pre-commit**. With [uv](https://github.com/astral-sh/uv) you can avoid global installs:

```bash
uvx pre-commit install --install-hooks
uvx pre-commit run --all-files
```

Without uv:

```bash
pipx install pre-commit || python -m pip install --user pre-commit
pre-commit install --install-hooks
pre-commit run --all-files
```

Tips:
- Re-run on staged files only: `pre-commit run`
- Skip a hook once: `SKIP=markdownlint-cli2 pre-commit run`
- Update hook versions: `pre-commit autoupdate` (then commit the rev bumps)

## 3) Wire CI (copy‑paste)

Add `.github/workflows/pre-commit.yml`:

```yaml
name: pre-commit

on:
  pull_request:
    branches: [ develop ]
  push:
    branches: [ develop ]

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - name: Install pre-commit
        run: |
          python -m pip install --upgrade pip
          pip install pre-commit gitlint
      - name: Run pre-commit on all files
        run: pre-commit run --all-files --show-diff-on-failure
```

## 4) Common lint fixes

- **MD022/MD032**: add a blank line before/after headings and lists.
- **MD001**: don’t jump heading levels (keep `###` after `##`).
- **EOF/newlines**: ensure a trailing newline and consistent `lf`.

## 5) Policy vs. pragmatism

Prefer fixing content, but path‑specific ignores are OK when format is externally constrained (e.g., copied issue templates). Example:

```yaml
# .markdownlint-cli2.yaml
ignores: [
  "docs/issues/**"  # informal issue notes
]
```

## 6) Language add‑ons (optional)

- **Python**: add black/ruff hooks via their official pre-commit repos.
- **JS/TS**: add eslint/prettier via local hooks or run them in a separate job.

**Contract note:** keep CI fast; prefer formatters + light static checks first, then deeper tests as your codebase grows.
