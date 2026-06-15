# Helper Review

Result: PASS.

Accepted:

- `core/protocol/test_job.py` loads and parses the TestJob schema.
- Helper validation checks schema/helper alignment.
- Metadata-only TestJob records can be built and validated.
- Unknown optional fields are tolerated.
- Unknown required capabilities fail closed.
- Accepted artifacts are projected into additive TestJob JSON files.
- Status, projection, validation, future-work, and unfinished-work reports are written under `.aide/reports/test-job/`.
- Explicit non-capabilities are preserved.

The helper keeps runtime and mutation flags false for Test Broker runtime, async execution, submission, run, retry runtime, summarize runtime, scheduler, leases, supervisor, worker execution, WorkUnit claim/run/finish/repair, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, release, promotion, Gateway, network, GitHub mutation, and model/provider calls.
