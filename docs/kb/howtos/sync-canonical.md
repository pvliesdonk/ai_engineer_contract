---
doc_type: kb_page
doc_version: 2025-10-19.r1
title: Sync Canonical Contract and Tools
---

# Sync Canonical Contract and Tools

## Intent

- Keep your repository aligned with the canonical Engineering Contract (and optionally tool templates) via a small, reviewable PR.

## Dry Run and Defaults

```bash
python tools/sync_canonical_contract_and_tools_TEMPLATE.py --dry-run
```

- Defaults: contract-only, base = develop, source = latest canonical release tag.

## Pinning, Tools, and Capsule

```bash
# Pin to a specific tag/ref
    python tools/sync_canonical_contract_and_tools_TEMPLATE.py --source-ref ai_engineer_contract-v2.3.0

# Include canonical tool templates (*_TEMPLATE.py only)
python tools/sync_canonical_contract_and_tools_TEMPLATE.py --include-tools

# Sync the minimal AI capsule as well
python tools/sync_canonical_contract_and_tools_TEMPLATE.py --include-capsule
```

## Overwrite Safety

- The script writes provenance markers (synced sha) into synced files and refuses to overwrite when a different synced sha is detected.
- To override (use with care):

```bash
python tools/sync_canonical_contract_and_tools_TEMPLATE.py --force
```

## Configuration

- You can set defaults in `ai/sync.config.json`:

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
