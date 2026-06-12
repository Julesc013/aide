# Schema Review

Result: `PASS`

Schema path:

- `.aide/protocol/aide-evidence-packet.schema.json`

Verified facts:

- JSON parses.
- Schema is narrow and describes `EvidencePacket` object shape.
- Required top-level packet fields are `apiVersion`, `kind`, `metadata`, `spec`, and `status`.
- `kind` is constrained to `EvidencePacket` for packet objects.
- Metadata includes producer and compatibility fields.
- Spec includes `source_task_id`, `source_task_kind`, `subject`, `capability_label`, `claims`, `explicit_non_capabilities`, `artifacts`, and `validations`.
- Status includes `phase`, `validated`, `validation_errors`, and `validation_warnings`.
- The schema does not define WorkUnit, TestJob, Checkpoint, PromotionPolicy, ProviderAdapter, Service, or Commander.
- Full JSON Schema Draft 2020-12 execution is truthfully deferred; runtime uses a local minimal subset validator.

Runtime validation report:

- `.aide/reports/evidence-packet/validation.json`
- status: `PASS`
- schema_file_loaded: `true`
- schema_file_parsed: `true`
- schema_validation_executed: `true`
- schema_validation_mode: `minimal_json_schema_subset`
- schema_helper_alignment_status: `PASS`

Warning:

- `validation.json` omits the requested aliases `source_artifacts_checked` and `evidence_packets_written`, but includes equivalent `source_reports_checked` and `projections_written` fields.
