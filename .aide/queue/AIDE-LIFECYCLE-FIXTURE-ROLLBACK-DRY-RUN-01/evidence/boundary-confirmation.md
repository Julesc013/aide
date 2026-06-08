# Boundary Confirmation

Allowed paths used:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01/**`
- `.aide/reports/lifecycle-fixture-rollback-dry-run/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- deterministic report refreshes under `.aide/reports/task-os-*`, `.aide/reports/lifecycle-schema-*`, `.aide/reports/scoped-transaction-executor-*`, `.aide/reports/managed-section-*`, `.aide/reports/transaction-*`, and `.aide/reports/current-aide-roadmap.md`

Protected paths preserved:

- `.git/**`
- `.github/**`
- `.aide.local/**`
- `.env`, `.env.*`
- `secrets/**`, `credentials/**`
- target repositories
- release publication files
- provider/model/Gateway integration files
- branch/worktree automation files
- rollback record files
- generated lifecycle fixture plans
- expected lifecycle reports
- static fixture target files
- lifecycle apply implementation files
- scoped transaction executor implementation files
- managed-section implementation files
- `core/**`

Forbidden operations preserved:

- install apply, upgrade apply, lifecycle repair apply, rollback apply, rollback execution, uninstall apply, uninstall execution, lifecycle apply, scoped transaction apply against fixture targets, fixture target mutation through apply, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, and release-ready claim.

Boundary search terms represented as blocked, deferred, report-only, non-goals, schema labels, or prohibited surfaces:

- install apply
- upgrade apply
- lifecycle repair apply
- rollback apply
- rollback execution
- uninstall apply
- uninstall execution
- dry-run
- report-only
- target_files_mutated
- rollback_apply_executed
- rollback_execution_implemented
- uninstall_apply_executed
- lifecycle_apply_executed
- scoped_transaction_apply_executed
- managed section
- preimage
- postimage
- allowed paths
- protected paths
- forbidden operations
- active repo
- target repo
- review gate
- needs_review
- production-ready
- release-ready
- broad active-repo apply
- provider/model calls
- Gateway calls
- network calls
