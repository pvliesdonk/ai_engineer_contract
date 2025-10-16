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

- Keep this contract at **`docs/design/ENGINEERING_CONTRACT.md`** and link back to the canonical repo.
- For KB/wiki work, store content under **`docs/kb/`** with an `index.md` and structured links.
- Open issues for work items; link PRs to issues; reference design docs where applicable.
- Use the script templates in `tools/` when operating in **SCM-C** (chat-only). In SCM-A, the AI can commit/push/PR directly (merge to `develop` needs chat approval; releases to `main` are manual).

## 3) Agents.md

- This repo includes a root [AGENTS.md](AGENTS.md) describing how AI agents should operate here.
- The root file applies repo-wide; nested `AGENTS.md` files may refine rules for subtrees.
- Human instructions in issues/PRs/chats take precedence over `AGENTS.md` files.

## 4) Branches & Releases

- Development happens on `develop` only; `main` is for releases.
- Releases are managed via release-please; after releasing on `main`, back-merge `main → develop` (workflow included).

## 5) Structure

- Contract: `docs/design/ENGINEERING_CONTRACT.md`
- Design docs: `docs/design/` (requirements, architecture, ADRs, roadmap)
- Knowledge base: `docs/kb/` with `index.md`
- AI manifest: `ai/manifest.json` (paths, base branch, labels, doc versioning scheme)
- Templates and tools: `templates/`, `tools/`

## 6) CI

- Markdown lint via `markdownlint-cli2` using `.markdownlint-cli2.yaml` and `.markdownlintignore`.
- Python helper scripts byte-compiled in CI.
- Release automation via release-please; backmerge workflow keeps `develop` in sync after releases.
