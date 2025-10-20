# Security Policy

## Supported Versions
This repository publishes a canonical contract and example tooling. Security fixes are applied on a best‑effort basis to the default branch.

## Reporting a Vulnerability
Please **do not file public issues** for security problems. Instead, use one of the following private channels:

1. **GitHub Security Advisories (preferred)** — Create a private advisory from the repo’s Security tab. This allows a coordinated, private discussion and patch.
2. **Email (fallback)** — If advisories are unavailable, contact the maintainer privately and include reproduction details and impact. Avoid sharing secrets or exploit code in plaintext.

We aim to acknowledge new reports within **3 business days** and provide a remediation plan or status update within **10 business days**.

## Disclosure Policy
- We prefer **coordinated disclosure**.
- If an issue affects downstream consumers of the contract/tools, we will document mitigations in the release notes.

## Hardening Notes
- Never commit secrets. Use `.env.example` to document required variables.
- Review CI logs for sensitive output.
- Prefer least‑privilege tokens for automation.
