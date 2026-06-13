# Prompt: AIDE-BUILD-WORKUNIT-CLI-01

Proceed with `AIDE-BUILD-WORKUNIT-CLI-01`.

Build only the first read-only WorkUnit CLI surface:

- `py -3 .aide/scripts/aide_lite.py workunit status`
- `py -3 .aide/scripts/aide_lite.py workunit list`
- `py -3 .aide/scripts/aide_lite.py workunit inspect --task-id <TASK_ID>`
- `py -3 .aide/scripts/aide_lite.py workunit validate`

Capability label: `minimal_workunit_readonly_cli`.

Do not implement `workunit create`, `claim`, `run`, `block`, `finish`, `repair`, runtime scheduling, WorkerRun, TestJob, Test Broker, Service, Commander, provider adapters, branch/worktree automation, target repo apply, active repo apply, rollback execution, release, promotion, network, Gateway, GitHub, or model/provider calls.

End at `needs_review`.
