# Schema Review

Status: PASS_WITH_WARNINGS.

`.aide/protocol/aide-worker-run.schema.json` exists, parses as JSON, declares `kind: WorkerRun`, uses the AIDE envelope shape, requires `apiVersion`, `kind`, `metadata`, `spec`, and `status`, and includes compatibility metadata plus provider, adapter, and run-mode metadata fields.

The schema does not require real worker execution. Current validation tolerates additive unknown optional fields and fails closed for unknown required capabilities through the helper/runtime validation path.

Warning: full JSON Schema Draft 2020-12 validation remains deferred; current validation uses the accepted local subset validator.
