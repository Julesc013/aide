# Fixture Tests

## Fixture Roots

- Direct no-overwrite copy fixtures: `%TEMP%/aide-qcheck04-_o6hjt8_`
- Import dry-run fixtures: `%TEMP%/aide-qcheck04-importdry-_hf7bvq_`
- Import apply validation fixture: `%TEMP%/aide-qcheck04-importapply-oj_wrydd`

Fixtures are outside the source repository and were left for inspection.

## Fresh Fixture

Raw payload copy:

- copied 629 pack files
- `doctor`: failed
- `validate`: failed
- reason: raw copy does not create target-specific memory/managed setup

Safe import:

- `import-pack --mode safe`: PASS
- `doctor`: PASS
- `validate`: PASS
- `install observe/plan/dry-run/validate`: PASS
- `upgrade observe/compare/plan/dry-run/validate`: PASS
- no target mutation beyond the isolated fixture import

## Existing-State Fixture

Seeded target-specific files:

- `.aide/memory/project-state.md`
- `.aide/queue/TARGET-OLD-TASK/status.yaml`
- `.aide/evals/golden-tasks/target-specific.yaml`
- `AGENTS.md`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/target-specific-report.md`

Safe import result:

- target memory preserved
- target queue preserved
- target golden task preserved
- target context packet preserved
- target report preserved
- `AGENTS.md` manual content preserved with AIDE managed section added

Lifecycle dry-runs:

- install dry-run: PASS
- upgrade dry-run: PASS
- repair dry-run: PASS
- rollback dry-run: PASS
- uninstall dry-run: PASS

## Unsafe Fixture

Seeded unsafe state:

- tracked `.aide.local/config.yaml`
- tracked `.env`
- unsupported schema marker
- source-state-like queue collision

Results:

- install observation reports blocking conflicts for `.aide.local`, `.env`, and unsupported schema
- repair plan blocks local state and marks unsupported schema as manual/future migration
- upgrade plan reports blocking local state, unsupported schema, source pack missing in fixture, and source-state contamination
- all unsafe operations keep `apply_allowed`, `overwrite_allowed`, and `delete_allowed` false

## Verdict

PASS_WITH_WARNINGS.

The pack is installable through safe import/preflight behavior. Raw payload copy is intentionally not considered a valid install mechanism.
