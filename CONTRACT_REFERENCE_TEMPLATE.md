# Engineering Contract (Canonical Reference)

This repository intentionally **references** the canonical contract instead of duplicating it.

- Canonical contract: https://github.com/pvliesdonk/ai_engineer_contract/blob/main/ENGINEERING_CONTRACT.md
- Tools: https://github.com/pvliesdonk/ai_engineer_contract/tree/main/tools

## Local Rules

- Base branch: `develop` by default. If this repository uses `development`, set `BASE_BRANCH=development` when running tools.
- Labels: `from-ai`, `needs-review`, `docs` (auto-created by tools if missing).

## Optional: Sync the canonical contract + tools into this repository

If you prefer the files to live in this repository, run:
```bash
# default (targets 'develop')
python tools/sync_canonical_contract_and_tools_TEMPLATE.py

# if your repo uses 'development' as the base branch
BASE_BRANCH=development python tools/sync_canonical_contract_and_tools_TEMPLATE.py
```
This opens a PR replacing `ENGINEERING_CONTRACT.md` and `tools/*` with the latest versions from the canonical repository.


