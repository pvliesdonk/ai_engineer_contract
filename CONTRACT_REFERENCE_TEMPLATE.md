# Engineering Contract (Canonical Reference)

## Intent

- Use this template when a repository references the canonical contract instead of duplicating it.
- Keep the repository’s automation tool-agnostic where possible; describe repo-specific tooling separately.
- Provide easy paths to sync the canonical contract and tools when desired.

- Canonical contract: [docs/design/ENGINEERING_CONTRACT.md](https://github.com/pvliesdonk/ai_engineer_contract/blob/main/docs/design/ENGINEERING_CONTRACT.md)
- Tools: [tools/](https://github.com/pvliesdonk/ai_engineer_contract/tree/main/tools)

## Local Rules

- Base branch: `develop` (always).
- Labels: `from-ai`, `needs-review`, `docs` (auto-created by tools if missing).

## Optional: Sync the canonical contract + tools into this repository

If you prefer the files to live in this repository, run:

```bash
# Always targets 'develop'
python tools/sync_canonical_contract_and_tools_TEMPLATE.py
```

This opens a PR replacing `ENGINEERING_CONTRACT.md` and `tools/*` with the latest versions from the canonical repository.

### Advanced (pin to a release tag, include tools/capsule)

```bash
# Pin to the latest canonical release tag (default), dry-run only
python tools/sync_canonical_contract_and_tools_TEMPLATE.py --dry-run

# Pin to a specific ref/tag and include canonical tool templates
    python tools/sync_canonical_contract_and_tools_TEMPLATE.py --source-ref ai_engineer_contract-v2.3.0 --include-tools

# Also sync the minimal AI capsule (optional)
python tools/sync_canonical_contract_and_tools_TEMPLATE.py --include-capsule

# Force overwrite if a different synced sha is detected in the target (use with care)
python tools/sync_canonical_contract_and_tools_TEMPLATE.py --force
```

Configuration file (optional): `ai/sync.config.json`

```json
{
  "sourceRepo": "pvliesdonk/ai_engineer_contract",
  "sourceRef": "latest",
  "syncContract": true,
  "syncTools": ["*_TEMPLATE.py"],
  "includeCapsule": false,
  "exclude": []
}
```
