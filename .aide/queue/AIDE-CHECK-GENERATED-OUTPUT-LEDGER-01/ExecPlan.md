# ExecPlan: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

## Purpose

Check `AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01` using repository artifacts,
focused tests, deterministic baseline replay, generated reports, and task-local
evidence.

## Scope

Allowed writes are limited to this task packet, task evidence, queue index
registration, and check reports under `.aide/reports/self-management/`.

This check does not repair, regenerate, delete, move, rename, normalize, or
rewrite any generated artifact, report, OKF page, context packet, source
reference, root, schema, queue record, or runtime/provider behavior.

## Current Facts

- The predecessor task is `needs_review`.
- The predecessor result is `PASS_WITH_WARNINGS`.
- The predecessor report records 1,381 candidates, 1,381 classified entries,
  67 unknown generators, and 9 findings: 4 info, 5 warnings, 0 errors, and 0
  blockers.
- A committed-tree replay at `af3156a` reproduced the 1,381 candidate count.
- A current-HEAD observation sees 1,385 candidates because ReportIndex added
  four generated report/index outputs after the ledger build.

## Milestones

1. Verify predecessor task status and evidence.
2. Verify implementation/test/report boundaries.
3. Reproduce the predecessor baseline and record current-HEAD observation.
4. Emit structured GovernanceFinding check records.
5. Run focused and broad validation.
6. Stop at `needs_review` with evidence.

## Validation Plan

- `py -3 -m unittest core.reconciler.tests.test_generated_output_ledger`
- `py -3 -m py_compile core/reconciler/generated_output_ledger.py core/reconciler/tests/test_generated_output_ledger.py`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01`
- JSON/YAML parse checks.
- Markdown/JSON finding agreement check.
- Diff checks before commit.

## Progress

- [x] Global preflight passed.
- [x] Predecessor task and evidence were inspected.
- [x] Focused tests and compile check passed.
- [x] Baseline replay and current-HEAD observation were recorded.
- [x] Check reports and evidence were written.
- [ ] Commit and post-commit validation.

## Recovery

If resumed, inspect `status.yaml`, rerun the validation commands above, and do
not continue if unexpected dirty state or error/blocker findings appear.

## Retrospective

The check preserved the predecessor warning debt and did not rewrite the ledger
to match current HEAD self-observation.
