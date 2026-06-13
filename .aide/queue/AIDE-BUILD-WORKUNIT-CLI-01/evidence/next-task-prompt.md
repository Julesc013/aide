# Next Task Prompt

Proceed with:

```text
AIDE-CHECK-WORKUNIT-CLI-01
```

Perform an independent check of `AIDE-BUILD-WORKUNIT-CLI-01`.

Review the read-only WorkUnit CLI slice for:

- `workunit status`
- `workunit list`
- `workunit inspect --task-id <TASK_ID>`
- `workunit validate`
- safe task-id handling and path confinement
- source queue task non-mutation
- additive report truthfulness
- unsupported mutation commands failing closed
- predecessor compatibility with lifecycle fixture runner, contract-envelope, EvidencePacket, and WorkUnit Queue V1
- no overclaiming and forbidden-operation preservation

Do not implement WorkUnit mutation commands, runtime scheduling, WorkerRun, TestJob, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target repo apply, active repo apply, rollback execution, release, promotion, network, Gateway, GitHub, or model/provider calls.

End with `PASS`, `PASS_WITH_WARNINGS`, `REJECTED_NEEDS_REPAIR`, `BLOCKED`, or `PARTIAL`.
