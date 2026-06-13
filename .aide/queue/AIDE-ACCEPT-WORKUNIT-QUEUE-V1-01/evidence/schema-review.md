# Schema Review

Result: `PASS`

Reviewed `.aide/protocol/aide-workunit.schema.json`.

The schema parses as JSON and remains narrow:

- `apiVersion`: `aide.dev/v1alpha1`
- `kind`: constrained to `WorkUnit`
- top-level shape: `apiVersion`, `kind`, `metadata`, `spec`, `status`
- required spec fields include `task_id`, `work_type`, `stop_state`, `scope`,
  `validation`, and `explicit_non_capabilities`
- required status fields include `phase`, `validated`, `validation_errors`, and
  `validation_warnings`

The schema does not define TestJob, Checkpoint, PromotionPolicy,
ProviderAdapter, Service, Commander, WorkerRun, Lease, or BranchAllocation.

Full JSON Schema Draft 2020-12 validation remains deferred by design.
