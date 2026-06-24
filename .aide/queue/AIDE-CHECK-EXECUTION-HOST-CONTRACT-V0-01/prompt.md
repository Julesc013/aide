# Prompt

Create and process
`AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01`.

Independently check `AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01`.

Verify that the ExecutionHost contract v0 is provider-neutral,
projection-only, keeps capability execution distinct from worker/session
execution, validates its schema/helper/projection records, preserves explicit
non-capabilities, and does not implement live host behavior, worker execution,
provider/model/network calls, Service/runtime behavior, Workbench behavior,
preview/apply/rollback, repository mutation, branch/worktree mutation, GitHub
mutation, release, or promotion.

If it passes, recommend exactly:

`AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01`

If material defects remain, recommend exactly:

`AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-REPAIR-01`

Do not repair implementation in this check task.
