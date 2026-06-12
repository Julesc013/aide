# Changed Files

## Code

- `core/protocol/evidence_packet.py`: minimal EvidencePacket helper, runtime
  validation, schema subset validation, accepted-slice projections, and report
  rendering.
- `core/protocol/__init__.py`: exposes the protocol helper module names.
- `.aide/scripts/aide_lite.py`: thin CLI loader and dispatch for
  `evidence-packet status`, `project`, and `validate`.

## Schema

- `.aide/protocol/aide-evidence-packet.schema.json`: minimal EvidencePacket
  schema aligned with the helper-required fields.

## Tests

- `.aide/scripts/tests/test_aide_evidence_packet_schema.py`: focused helper,
  schema, projection, CLI, compatibility, and overclaiming tests.

## Reports

- `.aide/reports/evidence-packet/status.md`
- `.aide/reports/evidence-packet/projection-report.json`
- `.aide/reports/evidence-packet/projection-report.md`
- `.aide/reports/evidence-packet/validation.json`
- `.aide/reports/evidence-packet/validation.md`
- `.aide/reports/evidence-packet/future-work.md`
- `.aide/reports/evidence-packet/unfinished-work.md`
- `.aide/reports/evidence-packet/projections/*.evidence-packet.json`

## Queue And Logs

- `.aide/queue/AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`
