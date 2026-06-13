# AIDE-BUILD-WORKUNIT-CLI-MUTATION-01 Prompt

Build only the low-risk WorkUnit queue metadata mutation CLI:

- `workunit create --from-spec <SPEC> --dry-run|--apply`
- `workunit block --task-id <TASK_ID> --reason <REASON> --note <NOTE> --dry-run|--apply`
- `workunit evidence add --task-id <TASK_ID> --path <PATH> --role <ROLE> --dry-run|--apply`

Do not implement claim, run, finish, repair, runtime, worker leases, scheduler, WorkerRun, TestJob, Test Broker, Service, Commander, providers, branch/worktree automation, target/active apply, rollback, release, promotion, network, Gateway, GitHub, or model/provider calls.
