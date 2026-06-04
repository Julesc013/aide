# Diagnosis

## Observed Stale State

- `.aide/queue/current.toml` is absent.
- `py -3 .aide/scripts/aide_lite.py task status` reports `latest_task_raw: AIDE-APPLY-02`, `latest_task_id: AIDE-APPLY-02`, and `latest_task_status: missing`.
- `.aide/context/latest-task-packet.md` still describes the older `AIDE-APPLY-02` setup context rather than the selected repair WorkUnit.
- `README.md` still names Q49 as the next AIDE-local work even though `AIDE-QUEUE-CLOSURE-02` selected this repair.
- Task OS next-selection logic still falls back to the older X-OS to `AIDE-APPLY-00 - Transaction Model` sequence.

## Cause

The latest task packet uses the shorthand `AIDE-APPLY-02`. After later queue work added multiple IDs beginning with that prefix, the shorthand is ambiguous and resolves to the raw token rather than the canonical scoped executor task. The Task OS report then treats the raw token as missing. Separately, the next-selection logic has not learned the accepted-with-notes `AIDE-APPLY-02` chain and still recommends the historical X-OS sequence.

## Repair Boundary

The repair is limited to Task OS status truth:

- exact current/latest task reporting;
- absent `current.toml` reporting;
- latest indexed task reporting;
- selected next WorkUnit reporting;
- historical and superseded task distinction;
- latest packet and README next-work truth;
- targeted Task OS tests and generated reports.

No apply, lifecycle apply execution, target mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply are authorized.
