# AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01 ExecPlan

## Purpose

Wire local validation for lifecycle manifest, lifecycle plan, lifecycle report, rollback-compatible lifecycle record, and fixture-shape examples created by `AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`.

## Scope

Allowed writes are limited to this task directory, queue index/latest packet, lifecycle schema/example files if validation repair is required, AIDE Lite validator code, one targeted validator test file, lifecycle-schema reports, deterministic status reports refreshed by required commands, README next-work text, and the lifecycle schema reference doc. No lifecycle apply, fixture target materialization, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply is authorized.

## Milestones

1. Verify live prerequisites and upstream task selection.
2. Create this queue scaffold and explicit allowed-path packet.
3. Add stdlib-only lifecycle-schema validator commands to AIDE Lite.
4. Validate schemas, examples, non-mutating mode, path boundaries, rollback-execution prohibition, and capability labels.
5. Add targeted unit tests.
6. Generate lifecycle-schema reports and task-local evidence.
7. Select the next safe WorkUnit without executing it.
8. Run validation, commit, and stop at `needs_review`.

## Non-Goals

- No lifecycle apply implementation or execution.
- No fixture target materialization.
- No install apply, upgrade apply, lifecycle repair apply, rollback apply, or uninstall apply.
- No active AIDE repo apply or target repo mutation.
- No branch/worktree mutation, merge, push, promotion, release publication, or GitHub mutation.
- No provider/model calls.
- No Gateway calls.
- No network calls.
- No broad active-repo apply.
- No production-ready or release-ready claim.

## Review Gate

End at `needs_review`. The selected next task is `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`, which may materialize fixture directories only if a future queue item explicitly authorizes that narrower work.
