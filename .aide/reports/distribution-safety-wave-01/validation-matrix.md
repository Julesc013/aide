# Validation Matrix

Every task should run a proportional subset of this matrix.

## Common

- JSON/YAML parse
- JSON Schema validation where schemas exist
- semantic helper validation where helpers exist
- `py_compile` or `compileall`
- focused unit tests
- fixture positive and negative cases
- object `status`, `project`, and `validate` commands where present
- migration commands where applicable
- DistributionManifest regression validation
- ProjectLock regression validation
- OwnershipLedger regression validation
- Q43-Q48 no-apply/no-publish validators
- task inspect
- task evidence
- `missing_evidence == 0`
- `material_finding_count == 0` for pass, acceptance, or successful repair-check results
- broad `py -3 .aide/scripts/aide_lite.py validate`
- local path scan
- secret-like scan
- source-output misuse scan
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## Fixture Apply Engine

- temp workspace isolation
- canonical fixture unchanged
- source repo unchanged
- target fixture copied before mutation
- rollback verification
- postimage digest verification
- manual content preservation
- unsafe operation refusal
