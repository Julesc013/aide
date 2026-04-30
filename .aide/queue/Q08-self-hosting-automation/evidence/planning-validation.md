# Q08 Planning Validation

Date: 2026-04-30

This evidence file records validation for creating the Q08 planning packet only. No Q08 implementation work, automation scripts, Harness logic, queue helper behavior, generated artifacts, Compatibility records, Dominium Bridge files, Runtime, Hosts, provider integrations, app surfaces, external CI, release automation, auto-merge, or autonomous service logic were created by this plan-only task.

## Dependency Gate

Q04 is `passed` in `.aide/queue/index.yaml`, and Q04 review outcome is `PASS_WITH_NOTES`.

Q05 remains `needs_review` in raw queue status, but `.aide/queue/Q05-generated-artifacts-v0/evidence/review.md` records final review outcome `PASS_WITH_NOTES`, and `.aide/queue/Q05-generated-artifacts-v0/evidence/review-recommendation.md` says Q06 planning may proceed.

Q06 remains `needs_review` in raw queue status, but `.aide/queue/Q06-compatibility-baseline/evidence/review.md` records final review outcome `PASS_WITH_NOTES`, and `.aide/queue/Q06-compatibility-baseline/evidence/review-recommendation.md` says Q07 planning may proceed.

Q07 is `passed` in `.aide/queue/index.yaml`, and Q07 review outcome is `PASS_WITH_NOTES`. `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-recommendation.md` says Q08 planning may proceed.

## Baseline Checks Before Planning Edits

Command: `py -3 scripts/aide validate`

Result: passed with warnings. Exit code `0`.

Observed summary:

```text
status: PASS_WITH_WARNINGS
summary: 142 info, 7 warning, 0 error
```

Expected warnings:

- Q00 through Q03 remain at raw review gates.
- Q05 and Q06 raw statuses remain at review gates even though review evidence records `PASS_WITH_NOTES`.
- `.aide/generated/manifest.yaml` reports `GENERATED-SOURCE-STALE` because source inputs changed after the last generated-artifact write.

Command: `py -3 scripts/aide doctor`

Result: passed with the same warning posture and no hard structural errors. It still reports `next_recommended_step: Q07 review...` even though Q07 is passed. Q08 plans a bounded fix before automation treats doctor output as an execution signal.

Command: `py -3 scripts/aide compile --dry-run`

Result: passed. It did not write files. It reports:

- `mutation: none`
- `.aide/generated/manifest.yaml: would_replace`
- managed sections and preview Claude output remain current
- Dominium Bridge target plan is metadata only

Command: `py -3 scripts/aide migrate`

Result: passed. Output reports the Q06 Compatibility baseline with no mutation:

```text
compatibility_baseline_version: aide.compat-baseline.v0
mutation: none
migration_engine: no-op-current-baseline
mutating_migrations_available: false
unknown_future_versions: error
migration_needed: false
```

Command: `py -3 scripts/aide bakeoff`

Result: passed. Output reports metadata/readiness only with no external calls and no executable bakeoff scenarios.

Command: `py -3 scripts/aide-queue-status`

Result: passed. Before the Q08 planning packet was written, Q08 reported `pending` with `planning_state: planned`.

Command: `py -3 scripts/aide-queue-next`

Result: passed. Before the Q08 planning packet was written, it reported Q08 as the next pending queue item.

## Planned Validation After Packet Creation

The following checks must be run after the Q08 planning files and queue index pointer are written:

- required Q08 file existence checks;
- `py -3 scripts/aide-queue-status`;
- `py -3 scripts/aide-queue-next`;
- `py -3 scripts/aide validate`;
- `py -3 scripts/aide doctor`;
- `py -3 scripts/aide compile --dry-run`;
- `py -3 scripts/aide migrate`;
- `py -3 scripts/aide bakeoff`;
- queue index reference check for Q08;
- ExecPlan section check;
- `git diff --check`;
- allowed-path audit.

## Results

## Required File Checks

Command:

```powershell
$files = @(
  '.aide/queue/Q08-self-hosting-automation/task.yaml',
  '.aide/queue/Q08-self-hosting-automation/ExecPlan.md',
  '.aide/queue/Q08-self-hosting-automation/prompt.md',
  '.aide/queue/Q08-self-hosting-automation/status.yaml',
  '.aide/queue/Q08-self-hosting-automation/evidence/planning-validation.md'
)
foreach ($f in $files) { if (Test-Path $f) { "OK $f" } else { "MISSING $f"; exit 1 } }
```

Result: passed. All required Q08 planning files exist.

## Queue Index Reference Check

Command:

```powershell
$patterns = @(
  'Q08-self-hosting-automation',
  '.aide/queue/Q08-self-hosting-automation/task.yaml',
  '.aide/queue/Q08-self-hosting-automation/ExecPlan.md',
  '.aide/queue/Q08-self-hosting-automation/prompt.md',
  '.aide/queue/Q08-self-hosting-automation/evidence'
)
foreach ($p in $patterns) {
  if (Select-String -Path .aide/queue/index.yaml -Pattern ([regex]::Escape($p)) -Quiet) { "OK $p" }
  else { "MISSING $p"; exit 1 }
}
```

Result: passed. Q08 is referenced with task, ExecPlan, prompt, and evidence paths.

## ExecPlan Section Check

Command checked the required section headings:

- Purpose
- Background And Current Repo Context
- Scope
- Non-goals
- Allowed Paths For Q08 Implementation
- Forbidden Paths For Q08 Implementation
- Self-Hosting Automation Model
- Automation Permission Model
- Queue Runner Model
- Evidence/Report Output Model
- Proposed-Task Model
- Known Carry-Forward Issues
- Drift/Status Reconciliation Plan
- Planned Deliverables
- Milestones
- Progress
- Surprises And Discoveries
- Decision Log
- Validation And Acceptance
- Idempotence And Recovery
- Evidence To Produce
- Outcomes And Retrospective

Result: passed. All required Q08 ExecPlan sections are present.

## Queue Checks

Command: `py -3 scripts/aide-queue-status`

Result: passed. Q08 reports `pending` with `planning_state: planning_complete`.

Command: `py -3 scripts/aide-queue-next`

Result: passed. Output reports `Q08-self-hosting-automation` with task and prompt paths.

## Harness Checks

Command: `py -3 scripts/aide validate`

Result: passed with warnings. Exit code `0`.

Observed summary after Q08 index update:

```text
status: PASS_WITH_WARNINGS
summary: 142 info, 7 warning, 0 error
```

Warnings are expected and unchanged in kind from baseline:

- Q00 through Q03 remain at raw review gates.
- Q05 and Q06 raw statuses remain at review gates despite accepted review evidence.
- `.aide/generated/manifest.yaml` remains source-fingerprint stale.

Command: `py -3 scripts/aide doctor`

Result: passed with warnings. It still reports the stale Q07 review next-step text, which Q08 explicitly plans to fix or avoid depending on.

Command: `py -3 scripts/aide compile --dry-run`

Result: passed. It ran in dry-run mode and wrote no files.

Observed generated artifact posture:

- `mutation: none`
- `.aide/generated/manifest.yaml: would_replace`
- managed sections remain current
- preview Claude output remains current
- final Claude targets remain deferred
- Dominium Bridge target plan remains metadata-only

Command: `py -3 scripts/aide migrate`

Result: passed. Output reports Q06 no-op current compatibility baseline and `migration_needed: false`.

Command: `py -3 scripts/aide bakeoff`

Result: passed. Output reports metadata/readiness only with no external calls and no executable bakeoff scenarios.

## Diff And Path Checks

Command: `git diff --check`

Result: passed. Git emitted line-ending normalization warnings for `.aide/queue/index.yaml` and `PLANS.md`; no whitespace errors were reported.

Allowed-path audit:

Changed or untracked paths are limited to:

- `.aide/queue/index.yaml`
- `.aide/queue/Q08-self-hosting-automation/**`
- `PLANS.md`

This is inside the plan-only allowed paths. No final automation scripts, Harness logic, queue helper behavior, generated artifacts, Compatibility records, Dominium Bridge files, Runtime, Hosts, provider/model/browser/app/release files, or Q09+ files were modified.
