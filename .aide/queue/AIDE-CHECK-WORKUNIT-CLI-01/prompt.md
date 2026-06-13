# Prompt: AIDE-CHECK-WORKUNIT-CLI-01

Check, do not build.

Independently review `AIDE-BUILD-WORKUNIT-CLI-01` and commit `721b3061e00d528b6c59386a1049048fbd9a339e`.

Verify:

- `workunit status`
- `workunit list`
- `workunit inspect --task-id <TASK_ID>`
- `workunit validate`
- unsupported mutation commands fail closed
- task id path safety
- source queue task traceability and non-mutation
- compatibility with accepted lifecycle fixture, contract-envelope, EvidencePacket, and WorkUnit Queue V1 layers
- no overclaiming and no forbidden operations

Do not implement WorkUnit mutation commands, runtime scheduling, WorkerRun, TestJob, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target repo apply, active repo apply, rollback execution, release, promotion, network, Gateway, GitHub mutation, or model/provider calls.

End at `needs_review`.
