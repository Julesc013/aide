# Accept Self-Management Charter

- task_id: AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01
- accepted_subject: AIDE self-management charter
- build_task_id: AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01
- check_task_id: AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01
- result: ACCEPTED_WITH_WARNINGS
- accepted_baseline: true
- recommended_next_task: AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

## Accepted Doctrine

```text
AIDE should clean up itself by protocol, not intuition.
```

```text
Observe -> Classify -> Compare -> Explain -> Plan -> Dry-run -> Validate
-> Review -> Apply only if authorized -> Record evidence -> Emit events
-> Update OKF -> Reconcile again.
```

## Accepted Warnings

| id | source | severity | accepted | next_task |
| --- | --- | --- | --- | --- |
| WARNING-001 | AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01 | warning | true | AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01 |
| WARNING-002 | AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01 | warning | true | AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01 |
| WARNING-003 | AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01 | warning | true | AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01 |

## Warning Disposition

- `WARNING-001`: `.aide/queue/index.yaml` line-ending warning is non-blocking.
- `WARNING-002`: unrelated prior commit-message warning is not charter evidence.
- `WARNING-003`: future Track B surfaces are intentionally deferred.

## Explicit Non-Capabilities

This acceptance does not implement or authorize formal GovernanceFinding schema,
GovernanceFinding CLI/helper/library, RootAuthorityManifest schema, doc truth
reconciler, generated-output ledger, OKF regeneration, root moves, file moves,
renames, reference rewrites, migration apply, runtime, provider/model/Gateway
behavior, GitHub/network behavior, branch/worktree automation, push, merge,
release, or target-repo mutation.

## Next

Proceed to:

`AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`

Keep it report-only first.
