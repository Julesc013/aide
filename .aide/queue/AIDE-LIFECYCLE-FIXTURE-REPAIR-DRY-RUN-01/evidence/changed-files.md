# Changed Files

This WorkUnit adds the `AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01` queue task, task-local evidence, report-only lifecycle fixture repair dry-run reports, queue index routing, and latest task packet routing.

Expected changed file groups:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01/**`: task scaffold, status, design, scenario matrix, no-apply proof, next-batch handoff, and evidence.
- `.aide/reports/lifecycle-fixture-repair-dry-run/**`: report-only repair dry-run check reports.
- `.aide/queue/index.yaml`: queue index entry for this WorkUnit.
- `.aide/context/latest-task-packet.md`: current task packet for this WorkUnit.
- `.aide/reports/task-os-*`, `.aide/reports/lifecycle-schema-*`, `.aide/reports/scoped-transaction-executor-*`, `.aide/reports/managed-section-*`, `.aide/reports/transaction-*`, `.aide/reports/current-aide-roadmap.md`: deterministic report refreshes from status/validation commands, if changed.

No generated repair plan, expected repair report fixture, fixture target, lifecycle apply implementation, scoped transaction executor implementation, provider/model/Gateway file, release file, branch/worktree automation file, or target repo file is changed by this task.
