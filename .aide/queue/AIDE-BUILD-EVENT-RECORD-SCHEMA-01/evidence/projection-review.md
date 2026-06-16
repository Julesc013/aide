# Projection Review

## Result

PASS_WITH_WARNINGS

## Reports

- `.aide/reports/event-record/projection-report.json`
- `.aide/reports/event-record/projection-report.md`
- `.aide/reports/event-record/event-family-index.json`
- `.aide/reports/event-record/event-family-index.md`
- `.aide/reports/event-record/example-events.json`
- `.aide/reports/event-record/example-events.md`

## Findings

- Event family count: 12.
- Example event count: 4.
- Source artifacts mutated during projection: false.
- Projection status: `PASS_WITH_WARNINGS`.
- Example events are projected report records only.

## Event Families

- WorkUnitStateChanged
- WorkerRunRecorded
- TestJobRecorded
- EvidencePacketRecorded
- AcceptanceRecorded
- ReferenceIDProjectionRecorded
- EventRecordProjectionRecorded
- CapabilityDeclared
- ConformanceResultRecorded
- OKFProjectionRecorded
- ReconcilerFindingRecorded
- PatchTransactionRecorded

All event families are marked `reserved_or_supported_for_schema` with `implemented_subsystem: false`.
