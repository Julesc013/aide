# EventRecord Event Family Index

- status: PASS_WITH_WARNINGS
- task_id: AIDE-BUILD-EVENT-RECORD-SCHEMA-01
- capability_target: minimal_event_record_schema
- event_family_count: 12
- implemented_subsystems: false

## Families

- WorkUnitStateChanged: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload
- WorkerRunRecorded: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload
- TestJobRecorded: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload
- EvidencePacketRecorded: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload
- AcceptanceRecorded: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload
- ReferenceIDProjectionRecorded: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload
- EventRecordProjectionRecorded: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload
- CapabilityDeclared: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload
- ConformanceResultRecorded: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload
- OKFProjectionRecorded: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload
- ReconcilerFindingRecorded: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload
- PatchTransactionRecorded: reserved_or_supported_for_schema; implemented_subsystem=false; payload_contract=minimal_open_payload

## Warnings

- Event family names reserve schema vocabulary only and do not implement their subsystems.
- EventRecord examples are projection-only and are not appended to a runtime store.
