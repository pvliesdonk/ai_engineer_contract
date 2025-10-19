SCM Mode Handshake
==================

1. **Auto-scan capabilities** (filesystem access, `git` push, `gh` auth). Infer SCM-A/B/C if possible.
2. **Ask once** when detection is inconclusive. Confirm before any privileged action (repo creation, default branch change, secret rotation).
3. **Log the mode** in the session notes or PR description. Record any switches with reason + timestamp.
4. **Consult the decision tree** at `docs/kb/howtos/scm-mode-decision-tree.md` before escalating privileges.
5. **Respect boundaries:** SCM-A may push/PR (merge with approval); SCM-B supplies ready-to-run instructions; SCM-C sticks to copy-paste flows.
