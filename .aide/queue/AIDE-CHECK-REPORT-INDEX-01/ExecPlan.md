# ExecPlan: AIDE-CHECK-REPORT-INDEX-01

## Purpose

Check `AIDE-BUILD-REPORT-INDEX-01` using repository artifacts, focused tests,
deterministic baseline replay, generated reports, and task-local evidence.

## Scope

Allowed writes are limited to this task packet, task evidence, queue index
registration, and check reports under `.aide/reports/self-management/`.

This check does not repair, move, rename, rewrite, normalize, delete, or migrate
any report or evidence reference, and does not start Track A or Track B B2.

## Current Facts

- The predecessor task is `needs_review`.
- The predecessor result is `PASS_WITH_WARNINGS`.
- The predecessor report records 479 indexed reports and 70 ambiguity records.
- A committed-tree replay at `bdfa1b7` reproduced the 479 report count and 70
  ambiguity records.
- A current-HEAD observation sees 484 reports because wave-2 ledger check and
  acceptance tasks added five report files after the ReportIndex build.

## Milestones

1. Verify predecessor task status and evidence.
2. Verify implementation/test/report boundaries.
3. Reproduce the predecessor baseline and record current-HEAD observation.
4. Emit structured GovernanceFinding check records.
5. Run focused and broad validation.
6. Stop at `needs_review` with evidence.

## Validation Plan

- `py -3 -m unittest core.reconciler.tests.test_report_index`
- `py -3 -m py_compile core/reconciler/report_index.py core/reconciler/tests/test_report_index.py`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-REPORT-INDEX-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-REPORT-INDEX-01`
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

The check preserved the predecessor warning debt and did not rewrite the index
to claim historic ledger acceptance.
