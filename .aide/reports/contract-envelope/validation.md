# Contract Envelope Validation

- status: PASS
- api_version: aide.dev/v1alpha1
- protocol_version: 0.1.0
- destructive_migration_performed: false
- backwards_compatibility_preserved: true

## Projections

- .aide/reports/contract-envelope/projections/lifecycle-fixture-acceptance.envelope.json
- .aide/reports/contract-envelope/projections/lifecycle-fixture-latest-run.envelope.json
- .aide/reports/contract-envelope/projections/lifecycle-fixture-verify.envelope.json

## Validation Results

- PASS: .aide/reports/contract-envelope/projections/lifecycle-fixture-acceptance.envelope.json
- PASS: .aide/reports/contract-envelope/projections/lifecycle-fixture-latest-run.envelope.json
- PASS: .aide/reports/contract-envelope/projections/lifecycle-fixture-verify.envelope.json

## Compatibility

- latest_run_json_parses: true
- verify_json_parses: true
- latest_run_top_level_status_scalar_preserved: true
- verify_top_level_status_scalar_preserved: true
- latest_run_legacy_capability_label_preserved: true
- verify_legacy_capability_label_preserved: true
- source_reports_destructively_migrated: false

## Warnings

- Minimal envelope helper is v1alpha1 and is not a full protocol stability claim.
- WorkUnit, EvidencePacket, TestJob, Checkpoint, ProviderAdapter, Service, and Commander schemas remain future work.
