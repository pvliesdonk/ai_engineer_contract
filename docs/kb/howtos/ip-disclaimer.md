---
doc_type: kb_page
doc_version: 2025-10-18.r1
title: IP Disclaimer & Rights Attestation Template
---

IP Disclaimer & Rights Attestation Template
===========================================

Intent
------

- Provide a reusable template for documenting intellectual property rights, quotation allowances, and citation expectations.
- Standardise how contributors attest to the rights they are asserting when adding source material.

Template Snippet
----------------

```markdown
# IP Disclaimer

We confirm that all contributed content complies with applicable IP policies.

- **Rights Attestation:** I have the right to submit this material. Extended quotations **are / are not** permitted under the following terms: `<license or agreement>`.
- **Citation Requirements:** Cite sources inline. For physical media include page spans (e.g., “pp. 42–47”). For web sources include permalinks and retrieval dates.
- **Third-Party Assets:** List any third-party assets (images, diagrams, audio) separately, including licence type and attribution text.
- **Policy Contact:** `<name/email>` for escalation when new rights questions arise.
```

Usage Guidelines
----------------

- Store the disclaimer in `IP_DISCLAIMER.md` at the repo root or under `docs/`.
- Require contributors to update the “Rights Attestation” line whenever they introduce quoted or derivative content.
- For AI-assisted content, include model/provider details and prompt summaries within the same disclaimer or an adjacent appendix.
- Use `templates/docs.kb.ip_disclaimer_template.md` as a starting point when creating new disclaimers.

Review Checklist
----------------

1. Does the submission state whether extended quotations are allowed?
2. Are page spans or timestamps provided for each citation?
3. Have third-party assets been inventoried with licence data?
4. Has the policy contact been verified recently?

Related References
------------------

- [Engineering Contract – IP Rights & Attestation](../../design/ENGINEERING_CONTRACT.md)
- [Dual Role – Canonical vs Instance Assets](../dual-role.md)
