# ai_engineer_contract

## 1) Summary

Canonical engineering contract for AI × Peter. Key points:
- **`develop`** is the only development branch. `main` is releases.
- Git-Flow style PRs; Conventional Commits; release automation (tool-agnostic).
- Deliverables as downloads; advice-only on request.
- Design-first: docs in `docs/design/`; KB/wiki in `docs/kb/` with an index.
- Docs use **date+rev**; releases use **SemVer**.
- Plan by **Milestones/Release Trains**, reconcile shipped tags in `docs/design/delivery-map.yml`.
- Self-contained & machine-readable (YAML front matter + `ai/manifest.json`).

## 2) How to use

- Keep this contract at **`docs/design/ENGINEERING_CONTRACT.md`** and link back to canonical repo.
- For KB/wiki work, store content under **`docs/kb/`** with an `index.md` and structured links.
- Open issues for work items; link PRs to issues; reference design docs where applicable.
- Use the script templates in `tools/` when operating in **SCM-C** (chat-only). In SCM-A, the AI can commit/push/PR directly (merge to `develop` needs chat approval; releases to `main` are manual).
