# WorkUnit CLI Validation

- status: PASS
- capability_label: minimal_workunit_readonly_cli
- workunit_cli_mode: readonly
- source_queue_tasks_checked: 116
- workunit_objects_validated: 116
- workunit_create_implemented: false
- workunit_claim_implemented: false
- workunit_run_implemented: false
- workunit_block_implemented: false
- workunit_finish_implemented: false
- workunit_repair_implemented: false
- source_queue_tasks_mutated: false
- destructive_migration_performed: false
- backwards_compatibility_preserved: true
- unknown_optional_fields_tolerated: true
- unknown_required_capability_fails_closed: true
- explicit_non_capabilities_preserved: true

## Path Safety

- path_traversal_rejected: true
- absolute_path_rejected: true
- separator_injection_rejected: true
- wildcard_rejected: true
- hidden_path_rejected: true

## Compatibility

- status: pass
- accepted_reports_parse: true
- legacy_queue_fields_preserved: true
- destructive_migration_performed: false
- lifecycle_fixture_behavior_preserved: true
- contract_envelope_behavior_preserved: true
- evidence_packet_behavior_preserved: true
- workunit_queue_behavior_preserved: true
- projections_additive: true

## Warnings

- This is a read-only CLI surface only; mutation, claim, run, finish, block, and repair remain unimplemented.
- Full JSON Schema Draft 2020-12 validation remains deferred to future conformance work.

## Future Work

- AIDE-CHECK-WORKUNIT-CLI-01: independent review of read-only WorkUnit CLI commands, path safety, compatibility, no destructive mutation, no overclaiming, and tests
- AIDE-BUILD-WORKUNIT-CLI-HARDEN-01: harden only if the check finds command, path, report, or compatibility gaps
- AIDE-ACCEPT-WORKUNIT-CLI-01: accept the read-only CLI after check and any required hardening
- AIDE-BUILD-WORKUNIT-CLI-MUTATION-01: add create/block-style mutation only after read-only CLI acceptance
- AIDE-BUILD-WORKER-RUN-SCHEMA-01: define WorkerRun before agent adapters
- AIDE-BUILD-TESTJOB-SCHEMA-01: define TestJob after the read-only WorkUnit CLI is accepted
