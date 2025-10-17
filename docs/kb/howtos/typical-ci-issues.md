---
doc_type: kb_page
doc_version: 2025-10-17.r1
title: Typical CI Issues (markdownlint) and Fixes
---

# Typical CI Issues (markdownlint) and Fixes

## Common Rules

- MD022: Headings should be surrounded by blank lines.
- MD032: Lists should be surrounded by blank lines.
- MD007: Unordered list indentation.
- MD005: Inconsistent indentation for list items.
- MD012: Multiple consecutive blank lines.

## Check and Fix Locally

```bash
# check
markdownlint-cli2 "**/*.md" "!**/node_modules/**" "!**/.git/**"

# fix
markdownlint-cli2 --fix "**/*.md" "!**/node_modules/**" "!**/.git/**"
```

## Troubleshooting

- Ensure `.markdownlint-cli2.yaml` and `.markdownlintignore` are present and match CI.
- Quote globs to avoid shell expansion issues.
- Consider pre-commit hooks for markdownlint to shorten feedback loops.
