# Q07 Planning Validation

Date: 2026-04-30

This evidence file records validation for creating the Q07 planning packet only. No Q07 implementation work, final bridge files, Dominium repository changes, Harness bridge checks, Compatibility implementation, generated Dominium outputs, Runtime, Hosts, provider integrations, app surfaces, release automation, or autonomous service logic were created by this plan-only task.

## Dependency Gate

Q04 is `passed` in `.aide/queue/index.yaml` and Q04 review outcome is `PASS_WITH_NOTES`.

Q05 remains `needs_review` in raw queue status, but `.aide/queue/Q05-generated-artifacts-v0/evidence/review.md` records final review outcome `PASS_WITH_NOTES`, and `.aide/queue/Q05-generated-artifacts-v0/evidence/review-recommendation.md` says Q06 planning may proceed.

Q06 remains `needs_review` in raw queue status, but `.aide/queue/Q06-compatibility-baseline/evidence/review.md` records final review outcome `PASS_WITH_NOTES`, and `.aide/queue/Q06-compatibility-baseline/evidence/review-recommendation.md` says Q07 planning may proceed.

Q05 and Q06 review tasks intentionally did not update `.aide/queue/index.yaml` because doing so would stale the Q05 generated manifest during review-only tasks.

## Planned Validation

The following checks must be run after the Q07 planning files and queue index pointer are written:

- required Q07 file existence checks;
- `py -3 scripts/aide-queue-status`;
- `py -3 scripts/aide-queue-next`;
- `py -3 scripts/aide validate`;
- `py -3 scripts/aide doctor`;
- `py -3 scripts/aide compile`;
- `py -3 scripts/aide migrate`;
- queue index reference check for Q07;
- ExecPlan section check;
- `git diff --check`;
- allowed-path audit.

## Results

## Required File Checks

Command:

```powershell
$files = @(
  '.aide/queue/Q07-dominium-bridge-baseline/task.yaml',
  '.aide/queue/Q07-dominium-bridge-baseline/ExecPlan.md',
  '.aide/queue/Q07-dominium-bridge-baseline/prompt.md',
  '.aide/queue/Q07-dominium-bridge-baseline/status.yaml',
  '.aide/queue/Q07-dominium-bridge-baseline/evidence/planning-validation.md'
)
foreach ($f in $files) { if (Test-Path $f) { "OK $f" } else { "MISSING $f"; exit 1 } }
```

Result: passed. All required Q07 planning files exist.

## Queue Checks

Command: `py -3 scripts/aide-queue-status`

Result: passed. Q07 reports `pending` with `planning_state: planning_complete`.

Command: `py -3 scripts/aide-queue-next`

Result: passed. Output reports `Q07-dominium-bridge-baseline` with task and prompt paths.

## Harness Baseline Checks

Command: `py -3 scripts/aide validate`

Result: passed with warnings. Exit code `0`.

Observed summary after Q07 index update:

```text
status: PASS_WITH_WARNINGS
summary: 109 info, 7 warning, 0 error
```

Expected warnings:

- Q00 through Q03 remain at review gates.
- Q05 raw status remains at review gate even though Q05 review evidence records `PASS_WITH_NOTES`.
- Q06 raw status remains at review gate even though Q06 review evidence records `PASS_WITH_NOTES`.
- `.aide/generated/manifest.yaml` reports `GENERATED-SOURCE-STALE` because Q07 planning updated `.aide/queue/index.yaml`, which is one of the Q05 manifest source inputs. This plan-only task is not allowed to refresh generated artifacts.

Command: `py -3 scripts/aide doctor`

Result: passed with the same expected warning posture and no hard structural errors.

Command: `py -3 scripts/aide compile`

Result: passed. It ran in dry-run mode and did not write files.

Observed generated artifact posture:

- managed sections remain current;
- preview Claude output remains current;
- final Claude targets remain deferred;
- `.aide/generated/manifest.yaml` would be replaced if `compile --write` were run, because the queue index changed.

Command: `py -3 scripts/aide migrate`

Result: passed. Output reports the Q06 Compatibility baseline:

```text
compatibility_baseline_version: aide.compat-baseline.v0
mutation: none
migration_engine: no-op-current-baseline
mutating_migrations_available: false
unknown_future_versions: error
q06_compatibility_baseline: implemented-v0
migration_needed: false
```

## Queue Index Reference Check

Command:

```powershell
Select-String -Path .aide/queue/index.yaml -Pattern 'Q07-dominium-bridge-baseline|.aide/queue/Q07-dominium-bridge-baseline/task.yaml|.aide/queue/Q07-dominium-bridge-baseline/ExecPlan.md|.aide/queue/Q07-dominium-bridge-baseline/prompt.md|.aide/queue/Q07-dominium-bridge-baseline/evidence'
```

Result: passed. Q07 is referenced with task, ExecPlan, prompt, and evidence paths.

## ExecPlan Section Check

Command checked the required section headings:

- Purpose
- Background And Current Repo Context
- Scope
- Non-goals
- Allowed Paths For Q07 Implementation
- Forbidden Paths For Q07 Implementation
- Dominium Bridge Scope
- XStack Boundary
- Stack Ordering
- Profile Overlay Model
- Policy Overlay Model
- Generated-Target Expectation Model
- Compatibility/Pinning Model
- Harness Validate/Doctor/Compile Bridge Behavior
- Planned Deliverables
- Milestones
- Progress
- Surprises And Discoveries
- Decision Log
- Validation And Acceptance
- Idempotence And Recovery
- Evidence To Produce
- Outcomes And Retrospective

Result: passed. All required Q07 ExecPlan sections are present.

## Diff And Path Checks

Command: `git diff --check`

Result: passed. Git emitted line-ending normalization warnings for `.aide/queue/index.yaml` and `PLANS.md`; no whitespace errors were reported.

Allowed-path audit:

Initial result: failed because Harness commands created Python `__pycache__` bytecode under `core/compat/` and `core/harness/`. Those cache files were local validation byproducts, not task outputs, and were removed after checking they were inside the repository.

Final result: passed. Changed paths are limited to:

- `.aide/queue/index.yaml`
- `.aide/queue/Q07-dominium-bridge-baseline/**`
- `PLANS.md`

## Plan-Only Non-Implementation Check

No final `bridges/dominium/**`, `.aide/**` contract records outside the Q07 planning folder, Harness implementation, Compatibility implementation, generated artifact, Dominium repository, Runtime, Host, provider, app, packaging, release, or Q08+ implementation files were modified by this plan-only task.
