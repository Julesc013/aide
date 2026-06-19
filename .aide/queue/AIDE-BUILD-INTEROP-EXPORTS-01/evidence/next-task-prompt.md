# AIDE-CHECK-INTEROP-EXPORTS-01

Create and process `AIDE-CHECK-INTEROP-EXPORTS-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read the live
repository before writing anything.

This is an independent check-only task for
`AIDE-BUILD-INTEROP-EXPORTS-01`.

Verify static preview artifacts, artifact hashes, report consistency, complete
task evidence, explicit non-capabilities, and absence of live MCP/A2A,
provider/model/network, worker, runtime, Host Contract, Dominium Bridge,
Workbench, PatchTransaction apply, branch/worktree, GitHub, release, promotion,
or target-repository mutation behavior.

Stop at `needs_review`.

If no material finding exists, recommend:

```text
AIDE-ACCEPT-INTEROP-EXPORTS-01
```
