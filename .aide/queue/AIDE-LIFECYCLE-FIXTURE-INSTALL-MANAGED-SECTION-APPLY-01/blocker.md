# Blocker

Blocker: `BLOCKED_MISSING_FIXTURE_APPLY_AUTHORITY`

The upstream gate selected this future task but did not authorize apply execution.

Authoritative evidence:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/task.yaml` records `apply_authorized_by_this_gate: false`.
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/status.yaml` records `apply_authorized_by_this_gate: false`.
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/next-batch.md` states the gate does not itself authorize execution.
- The attached prompt pack requires explicit gate authority before running the first fixture apply.

No apply was run.
