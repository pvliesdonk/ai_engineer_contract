# CONTRIBUTING

- Branch from `origin/develop` using `feat/<slug>` or `fix/<slug>`.
- Use **Conventional Commits** for PR titles; include Summary/Why/Changes/Validation/Risk/Notes.
- Keep docs updated in `docs/design/` and `docs/kb/`.
- Releases are created via the configured release tool; merges to `main` are manual.

## Syncing the Canonical Contract (Consumers)

- Use the sync helper to update `ENGINEERING_CONTRACT.md` (and optionally tool templates/capsule) via a small PR.
- Safety first: run a dry run, pin to a release tag, and avoid `--force` unless you understand the overwrite warning.
- See: `docs/kb/howtos/sync-canonical.md` and `ai/sync.config.json` for defaults.
