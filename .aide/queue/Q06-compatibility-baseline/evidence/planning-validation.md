# Q06 Planning Validation

Date: 2026-04-30

This evidence file records validation for creating the Q06 planning packet only. No Q06 implementation work, final compatibility records, Harness compatibility code, generated artifact behavior changes, Dominium Bridge behavior, Runtime, Hosts, provider integrations, app surfaces, release automation, or autonomous service logic were created by this plan-only task.

## Dependency Gate

Q04 is `passed` in `.aide/queue/index.yaml` and Q04 review outcome is `PASS_WITH_NOTES`.

Q05 remains `needs_review` in raw queue status, but `.aide/queue/Q05-generated-artifacts-v0/evidence/review.md` records final review outcome `PASS_WITH_NOTES`, and `.aide/queue/Q05-generated-artifacts-v0/evidence/review-recommendation.md` says Q06 planning may proceed. Q05 review intentionally did not update `.aide/queue/index.yaml` because doing so would stale the Q05 generated manifest during a review-only task.

## Planned Validation

The following checks must be run after the Q06 planning files and queue index pointer are written:

- required Q06 file existence checks;
- `py -3 scripts/aide-queue-status`;
- `py -3 scripts/aide-queue-next`;
- `py -3 scripts/aide validate`;
- `py -3 scripts/aide doctor`;
- `py -3 scripts/aide migrate`;
- queue index reference check for Q06;
- ExecPlan section check;
- `git diff --check`;
- allowed-path audit.

## Results

## Required File Checks

Command:

```powershell
$files = @(
  '.aide/queue/Q06-compatibility-baseline/task.yaml',
  '.aide/queue/Q06-compatibility-baseline/ExecPlan.md',
  '.aide/queue/Q06-compatibility-baseline/prompt.md',
  '.aide/queue/Q06-compatibility-baseline/status.yaml',
  '.aide/queue/Q06-compatibility-baseline/evidence/planning-validation.md'
)
foreach ($f in $files) { if (Test-Path $f) { "OK $f" } else { "MISSING $f"; exit 1 } }
```

Result: passed. All required Q06 planning files exist.

## Queue Checks

Command: `py -3 scripts/aide-queue-status`

Result: passed. Q06 reports `pending` with `planning_state: planning_complete`.

Command: `py -3 scripts/aide-queue-next`

Result: passed. Output reports `Q06-compatibility-baseline` with task and prompt paths.

## Harness Baseline Checks

Command: `py -3 scripts/aide validate`

Result: passed with warnings. Exit code `0`.

Observed summary after Q06 index update:

```text
status: PASS_WITH_WARNINGS
summary: 75 info, 6 warning, 0 error
```

Expected warnings:

- Q00 through Q03 remain at review gates.
- Q05 raw status remains at review gate even though Q05 review evidence records `PASS_WITH_NOTES`.
- `.aide/generated/manifest.yaml` reports `GENERATED-SOURCE-STALE` because Q06 planning updated `.aide/queue/index.yaml`, which is one of the Q05 manifest source inputs. This plan-only task is not allowed to refresh generated artifacts.

Command: `py -3 scripts/aide doctor`

Result: passed with the same expected warning posture and no hard structural errors.

Command: `py -3 scripts/aide migrate`

Result: passed. Output remains the Q04/Q05 no-op baseline:

```text
mode: no-op baseline report
profile_contract_version: aide.profile-contract.v0
compat_schema_status: baseline
migration_baseline_status: placeholder
migration_engine: not implemented
automatic_migrations: none
q06_compatibility_baseline: deferred
```

Command: `py -3 scripts/aide compile`

Result: passed. It ran in dry-run mode and did not write files.

Observed generated artifact posture:

- managed sections remain current;
- preview Claude output remains current;
- final Claude targets remain deferred;
- `.aide/generated/manifest.yaml` would be replaced if `compile --write` were run, because the queue index changed.

## Queue Index Reference Check

Command:

```powershell
Select-String -Path .aide/queue/index.yaml -Pattern 'Q06-compatibility-baseline|.aide/queue/Q06-compatibility-baseline/task.yaml|.aide/queue/Q06-compatibility-baseline/ExecPlan.md|.aide/queue/Q06-compatibility-baseline/prompt.md|.aide/queue/Q06-compatibility-baseline/evidence'
```

Result: passed. Q06 is referenced with task, ExecPlan, prompt, and evidence paths.

## ExecPlan Section Check

Command checked the required section headings:

- Purpose
- Background And Current Repo Context
- Scope
- Non-goals
- Allowed Paths For Q06 Implementation
- Forbidden Paths For Q06 Implementation
- Compatibility Scope
- Version Model
- Migration Model
- Replay Baseline Model
- Upgrade Gate Model
- Deprecation Model
- Harness Migrate/Validate Changes
- Planned Deliverables
- Milestones
- Progress
- Surprises And Discoveries
- Decision Log
- Validation And Acceptance
- Idempotence And Recovery
- Evidence To Produce
- Outcomes And Retrospective

Result: passed. All required Q06 ExecPlan sections are present.

## Diff And Path Checks

Command: `git diff --check`

Result: passed. Git emitted a line-ending normalization warning for `.aide/queue/index.yaml`; no whitespace errors were reported.

Allowed-path audit:

Initial result: failed because `py -3 scripts/aide validate` created Python `__pycache__` bytecode under `core/harness/`. Those cache files were local byproducts of validation, not task outputs, and were removed after checking they were inside the repository.

Final result: passed. Changed paths are limited to:

- `.aide/queue/index.yaml`
- `.aide/queue/Q06-compatibility-baseline/**`

## Plan-Only Non-Implementation Check

No final `core/compat/**`, `.aide/compat/**`, Harness implementation, generated artifact, contract, policy, host, bridge, runtime, provider, app, packaging, release, or Q07+ implementation files were modified by this plan-only task.
