# QFIX-01 Prompt Summary

Implement a bounded state reconciliation after the
`QCHECK-token-survival-foundation-audit` checkpoint.

Required outcomes:

- Review Q09-Q20 and classify them.
- Reconcile queue index/status/evidence truth.
- Fix Q18 status drift.
- Update `.aide/profile.yaml` so current focus reflects post-token-survival
  reconciliation, not stale Q09 work.
- Update `.aide/commands/catalog.yaml` and self-check guidance without
  overclaiming live Gateway/provider behavior.
- Compactly update README, ROADMAP, PLANS, IMPLEMENT, and DOCUMENTATION.
- Write QFIX-01 evidence and stop at `needs_review`.

Explicitly forbidden:

- QFIX-02 test discovery fixes.
- Q21 export/import or tool adapter work.
- Gateway forwarding, provider calls, model calls, runtime/UI work, autonomous
  loops, secrets, raw prompt logs, raw response logs, or `.aide.local/` state.
