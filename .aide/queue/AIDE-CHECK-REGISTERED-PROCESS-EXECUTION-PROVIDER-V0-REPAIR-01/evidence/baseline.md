# Baseline

- Branch state at intake: `main...origin/main`.
- Worktree state at intake: clean.
- Queue policy: `concurrency.default: 1`.
- Source repair task: `AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`.
- Source repair commit: `7f043d09ae0c5bbb73d68ad293e6dafaaaa8ddd6`.
- Source repair result: `PASS_WITH_WARNINGS`.
- Source failed check: `AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01`.
- Source failed check result: `REQUEST_CHANGES` with five material findings.
- This check task did not exist before this run and was materialized under its own queue packet.

Allowed mutation for this check is limited to the task packet, task-local check
reports, queue index, and root planning/execution logs.

Implementation repair, provider acceptance, live Dominium command rerun,
Dominium or target-repository mutation, worker/runtime/Workbench behavior,
provider/model/network calls, preview/apply/rollback, GitHub mutation, branch or
worktree creation, release, and promotion are out of scope.
