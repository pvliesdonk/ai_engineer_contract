# AI × Peter — Engineering Contract & Working Agreement (v1.0.0)

**Effective:** 2025-10-14 08:48:39 UTC  
**Owner:** Peter van Liesdonk (GitHub: `pvliesdonk`)  
**Scope:** This contract governs how we (you = AI assistant; I = Peter) collaborate on software and docs.
Embed this file as a *Project Prompt* so the assistant always follows it.

---

## 1) Repository & Branching

- **All work lives in** `pvliesdonk/{repo_name}` on GitHub.
- **Default branches:**
  - `main` → release-only. Only updated via PR from `develop` when I explicitly ask for a release.
  - `develop` → active development; base for all PRs.
- **Feature/fix branch naming:**
  - `feat/<slug>` new capability; `fix/<slug>` bug fix; `chore/<slug>` infra/ops; `docs/<slug>` docs; `refactor/<slug>` refactor; `test/<slug>` tests.
- **Small fixes** always in their own branch; open a PR into `develop`.

## 2) Sync & Rebase Discipline

- **Always base work on** the latest `origin/develop` (fetch first).
- **No merge commits** in feature branches. Rebase onto `origin/develop` before opening a PR.
- **PR merges:** use **Squash & merge** into `develop` (single, clean history).

## 3) Pull Request Quality Bar

Each PR must be **review-ready** and **self-contained**:

- Clear, specific title (Conventional Commits style, e.g., `feat: add config loader`).
- Concise body with context, what/why, risk surface, and test/validation notes.
- Update docs and examples when behavior or interfaces change.
- Keep diffs small and purposeful. Prefer multiple small PRs over one mega-PR.
- Run/describe local checks (lint/tests/build) and include repro steps when relevant.
- Avoid secrets in code, diffs, logs, or PR text. Redact tokens/URLs/IDs.

### PR Body Template (for squash merges)

```
# Summary
What this PR does in one crisp paragraph.

# Why
Reasoning, tradeoffs, alternatives considered.

# Changes
- Bullet points of key modifications.

# Validation
- How it was tested (commands, screenshots, logs).

# Risk & Rollback
- Expected impact, failure blast radius, quick rollback steps.

# Notes for Reviewer
- Pointers to tricky parts, follow-ups, or scope boundaries.
```

## 4) Release Process (when I say so)

- Open a PR **`develop → main`** titled `release: vX.Y.Z`.
- Ensure version bump and CHANGELOG are present (auto-generate if we have tooling; otherwise summarize notable changes).
- After merge, tag `vX.Y.Z` and create a GitHub Release with the changelog body.
- Keep `develop` ahead of `main` (no direct commits to `main`).

## 5) Access Modes

- **Direct GitHub access available** (e.g., via MCP or IDE plugin): create branches and PRs directly in `pvliesdonk/{repo_name}` following this contract.
- **No direct access:** emulate the same flow by delivering a **single-file PR script** (see §6) that uses the GitHub CLI (`gh`) and `git` to:
  - clone `pvliesdonk/{repo_name}` to `/mnt/scratch/…`,
  - branch off **`origin/develop`**,
  - apply the embedded **unified diff** (and optional file blobs),
  - commit, push, and **open a PR** against `develop` with labels and a ready-to-squash body.

## 6) PR Script Requirements (emulated mode)

When you don’t have direct write access, you must deliver a script that:
- is a **single file** that users can run locally,
- contains the **diff embedded inside** (no extra files needed),
- uses `/mnt/scratch` for its working directory,
- relies on `git` and **GitHub CLI (`gh`)** (assume `gh auth status` is already configured),
- **rebases** on `origin/develop` before committing,
- creates a **feature branch** (e.g., `feat/…`, `fix/…`),
- pushes to `origin` and opens a PR with a proper title/body/labels,
- exits non-zero with clear messaging on any error so it’s easy to diagnose.

A reference implementation is provided in `pr_from_diff_TEMPLATE.py` (included alongside this file).

## 7) Security & Secrets

- Never commit credentials, tokens, or endpoints that expose private systems.
- Default to `.gitignore` for creds and local dev files. Provide `.env.example` for env vars.
- If logs or artifacts might include sensitive values, demonstrate **redaction**.

## 8) Communication Contracts

- Keep progress logs **concise and factual**. No filler.
- When proposing changes, summarize impact and include the **exact commands** the reviewer can run.
- Prefer **deterministic** scripts and pinned versions for reproducibility.

## 9) Style & Conventions

- Titles: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`).
- Code style: obey project linters/formatters; if none exist, propose one in a separate PR.
- Commit message = PR title; detailed context lives in PR body (squash merge keeps it tidy).

## 10) Failure & Recovery

- If a step is ambiguous or blocks progress, propose **two concrete options** with tradeoffs and pick a default.
- If we lose conversation context, recover from the repo state and this contract.

---

### Appendix A — Minimal Command Cheatsheet

```bash
git fetch --all --prune
git checkout develop && git reset --hard origin/develop
git switch -c feat/<slug>
# ... apply changes ...
git add -A && git commit -m "feat: <title>"
git push -u origin HEAD
gh pr create --base develop --title "feat: <title>" --body-file pr.md --label from-ai --label needs-review
```

### Appendix B — Labels we may use

- `from-ai`, `needs-review`, `blocked`, `security`, `breaking-change`, `docs`, `chore`

---

**This contract supersedes prior ad-hoc arrangements; updates will be versioned in this file.**
