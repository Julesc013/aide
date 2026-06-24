# AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01

Create and process `AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01`.

Build a provider-neutral, projection-only contract for bounded worker/session
execution hosts.

Keep capability execution and worker execution distinct. Do not implement a live
ExecutionHost, LocalProcessExecutionHost, Omnigent, worker execution,
provider/model/network calls, Service/runtime behavior, Workbench behavior,
preview/apply/rollback, repository mutation, branch/worktree mutation, GitHub
mutation, release, or promotion.

Stop at `needs_review` and recommend exactly:

```text
AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01
```
