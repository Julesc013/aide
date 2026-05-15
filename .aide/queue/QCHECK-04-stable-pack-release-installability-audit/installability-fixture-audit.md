# Installability Fixture Audit

## Fixture 1: Fresh Repo

Direct payload-copy fixture:

- Root: `%TEMP%/aide-qcheck04-_o6hjt8_/fresh`
- Copied pack `files/**` with no overwrite.
- `doctor`: failed.
- `validate`: failed.
- Cause: direct copy lacks import-generated target memory/managed setup.
- Classification: expected fixture limitation, not pack invalidity.

Safe import fixture:

- Root: `%TEMP%/aide-qcheck04-importapply-oj_wrydd/fresh-apply`
- Command family: local `import-pack --mode safe` from local release archive/export pack.
- `doctor`: PASS.
- `validate`: PASS.
- `install dry-run`: PASS, planned writes 0, no target mutation.
- `upgrade dry-run`: PASS, planned updates 0, no target mutation.

## Fixture 2: Existing Target State

Fixture state:

- `.aide/memory/project-state.md`
- `.aide/queue/TARGET-OLD-TASK/status.yaml`
- `.aide/evals/golden-tasks/target-specific.yaml`
- `AGENTS.md` manual content
- `.aide/context/latest-task-packet.md`
- `.aide/reports/target-specific-report.md`

Safe import result:

- Root: `%TEMP%/aide-qcheck04-importapply-oj_wrydd/existing-apply`
- Target memory: preserved.
- Target queue: preserved.
- Target golden task: preserved.
- Target latest task packet: preserved.
- Target report: preserved.
- `AGENTS.md`: manual content preserved; AIDE managed section added.

Lifecycle dry-runs:

- `install dry-run`: PASS, planned writes 0, conflicts preserved.
- `upgrade dry-run`: PASS, planned updates 0.
- `repair dry-run`: PASS, planned writes 1, no apply.
- `rollback dry-run`: PASS, planned restores 0, removals 0.
- `uninstall dry-run`: PASS, future removal candidates 274, no delete/apply.

## Fixture 3: Unsafe Target State

Fixture state:

- tracked `.aide.local/config.yaml`
- `.env` with example key-shaped text
- `.aide/policies/legacy.yaml` with unsupported schema marker
- `.aide/queue/SOURCE-COPIED/status.yaml`

Observed results:

- Install observation reports blocking conflicts for tracked `.aide.local`, `.env`, and unsupported schema.
- Repair diagnosis reports tracked local state and unsupported schema.
- Repair plan blocks `.aide.local/config.yaml` and `.env`, marks unsupported schema manual review/future migration, and keeps `apply_allowed`, `overwrite_allowed`, and `delete_allowed` false.
- Upgrade comparison reports blocking conflicts for local state, unsupported schema, missing source pack in fixture, and source-state contamination.
- Upgrade plan marks mandatory migrations as future-only with `apply_allowed: false`.

## Cleanup Behavior

Fixture directories were created under system temp and left for inspection. They are outside the AIDE repository and are not committed.

## Verdict

PASS_WITH_WARNINGS.

Installability is supported through safe import and no-apply lifecycle planning. Raw payload copy is not an install path. Target-specific state preservation passed in the existing-state fixture, with managed-section changes requiring target review.
