# ai_engineer_contract

Canonical home for the **AI × Peter Engineering Contract** and the helper tools that keep repos tidy, auditable, and predictable.

- `ENGINEERING_CONTRACT.md` — the **canonical contract** (latest version lives in this repo).
- `tools/` — ready-to-run helpers:
  - `pr_from_diff_TEMPLATE.py` — open a PR from an embedded diff or file blobs.
  - `repo_bootstrap_TEMPLATE.py` — bootstrap/normalize a repo (license, branches, labels).
  - `sync_canonical_contract_and_tools_TEMPLATE.py` — update any repo to the latest contract/tools.

This repository is **not** a template repository; other projects should **link to it** and optionally sync files using the provided tools.

---

## Why this exists

We want a consistent, reviewable flow for both code and docs. The contract standardizes branching, PR quality, releases, deliverables, escaping, labels, and “advice-only” behavior.

---

## How other repositories should reference this contract

Most projects should **reference** the canonical contract instead of copy/pasting it. Add a small file named `ENGINEERING_CONTRACT.md` (or keep an existing one) that points to this repo:

> See the canonical contract: https://github.com/pvliesdonk/ai_engineer_contract/blob/main/ENGINEERING_CONTRACT.md

For convenience, you can drop in the provided template file from this repo: `CONTRACT_REFERENCE_TEMPLATE.md` (rename it to `ENGINEERING_CONTRACT.md` in your project).

If you want the latest contract + tools **checked in** to a repo (e.g., to make local edits or preserve a snapshot), use the sync tool below.

---

## Syncing contract + tools into another repo (optional)

### Default (targets `develop` as the base branch)
```bash
python tools/sync_canonical_contract_and_tools_TEMPLATE.py
```

### If your repo uses `development` instead of `develop`
```bash
BASE_BRANCH=development python tools/sync_canonical_contract_and_tools_TEMPLATE.py
```

The sync tool will:
- clone the repo to a scratch dir,
- create a branch from `origin/<BASE_BRANCH>`,
- replace `ENGINEERING_CONTRACT.md` and `tools/*` with the latest versions,
- commit and open a PR with labels `from-ai`, `needs-review`, `docs`.

---

## Branching & PR flow (short version)

- `main` — releases only (cut from the base branch on demand).
- **Base branch:** `develop` by default. If a repo uses `development`, set `BASE_BRANCH=development` when running tools.
- Always rebase on `origin/<BASE_BRANCH>` before opening PRs.
- Squash-merge PRs; use **Conventional Commits** for titles.
- PR body structure: **Summary**, **Why**, **Changes**, **Validation**, **Risk & Rollback**, **Notes**.

See full details in `ENGINEERING_CONTRACT.md`.

---

## “Advice-only” responses

When a user explicitly asks for **advice**, assistants return guidance/snippets/commands inline **without** packaging downloadable artifacts. Otherwise, deliverables must be provided as downloadable files.

---

## Releases

Releases are automated with **release-please** (manifest mode). Merge the Release PR to publish the tag and GitHub Release. See the Releases page for version history.

---

## License

MIT (see `LICENSE`).

