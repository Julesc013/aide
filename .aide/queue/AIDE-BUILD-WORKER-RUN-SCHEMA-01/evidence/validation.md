# Validation

## WorkerRun Commands

- `py -3 .aide/scripts/aide_lite.py worker-run status`: PASS
- `py -3 .aide/scripts/aide_lite.py worker-run project --source accepted-artifacts`: PASS, 5 projections, source reports not mutated
- `py -3 .aide/scripts/aide_lite.py worker-run validate`: PASS

`validation.json` confirms:

- schema_file_loaded: true
- schema_file_parsed: true
- schema_validation_executed: true
- schema_helper_alignment_status: PASS
- backwards_compatibility_preserved: true
- unknown_optional_fields_tolerated: true
- unknown_required_capability_fails_closed: true
- explicit_non_capabilities_preserved: true
- metadata_only_truthful: true

## AIDE Commands

- `py -3 .aide/scripts/aide_lite.py validate`: PASS
- `py -3 .aide/scripts/aide_lite.py test`: PASS
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-WORKER-RUN-SCHEMA-01`: PASS, classification complete, missing_evidence 0
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-WORKER-RUN-SCHEMA-01`: PASS, missing none

## WorkUnit CLI Compatibility

- `workunit status/list/inspect/validate`: PASS
- `workunit create --dry-run`: PASS, queue files written 0
- `workunit block --dry-run`: PASS, queue files written 0
- `workunit evidence add --dry-run`: PASS, queue files written 0
- `workunit claim/run/finish/repair`: fail closed with exit code 2
- `worker-run run`: fail closed with exit code 2

## Whitespace

- `git diff --check`: PASS with a non-blocking CRLF warning for `.aide/queue/index.yaml`.
