# Queue Prompt: AIDE-BUILD-REFERENCE-ID-SCHEME-01

Build the minimal ReferenceID scheme after accepted `minimal_test_job_schema`.

Use live `.aide/queue/` state as canonical authority. Materialize a queue task with an ExecPlan, bounded allowed paths, evidence, validation, and a `needs_review` stop state before implementation.

Expected scope:

- Define a minimal deterministic reference identifier scheme for protocol artifacts.
- Keep the scheme metadata-only and compatibility-first.
- Preserve accepted ContractEnvelope, EvidencePacket, WorkUnit Queue, WorkerRun, and TestJob behavior.
- Include explicit non-capabilities and fail-closed handling for unsupported or ambiguous identifier forms.
- Add focused tests and reports only within the task's authorized paths.

Do not implement PatchTransaction, EventRecord, Test Broker runtime, scheduler, leases, worker execution, Service, Commander, provider adapters, branch/worktree automation, target apply, active apply, rollback execution, release, GitHub mutation, Gateway, network calls, model/provider calls, production readiness, release readiness, or broad runtime behavior.

PatchTransaction is not the next task after TestJob acceptance. Follow `AIDE-BUILD-REFERENCE-ID-SCHEME-01` unless a later reviewed queue item changes live queue truth.
