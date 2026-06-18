# ExecPlan: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

## Purpose

Check `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01` using repository
artifacts, deterministic tests, generated reports, and task-local evidence.

## Scope

Allowed writes are limited to this task packet, task evidence, queue index
registration, and check reports under `.aide/reports/self-management/`.

This check does not repair documentation, OKF pages, context packets, path
references, generated outputs, reports, roots, schemas, queue state, or
runtime/provider behavior.

## Current Facts

- The predecessor task is `needs_review`.
- The predecessor result is `PASS_WITH_WARNINGS`.
- The predecessor report records 900 scanned paths and 12 findings:
  3 info, 9 warnings, 0 errors, and 0 blockers.
- This thread has prior build context available, so this check records a
  reduced-independence warning and uses mechanical repository verification.

## Milestones

1. Verify predecessor task status and evidence.
2. Verify implementation/test/report boundaries.
3. Emit structured GovernanceFinding check records.
4. Run focused and broad validation.
5. Stop at `needs_review` with evidence.

## Validation Plan

- `py -3 -m unittest core.reconciler.tests.test_doc_knowledge_truth`
- `py -3 -m py_compile core/reconciler/doc_knowledge_truth.py core/reconciler/tests/test_doc_knowledge_truth.py`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`
- JSON/YAML parse checks.
- Markdown/JSON finding agreement check.
- Diff checks before commit.

## Progress

- [x] Global preflight passed.
- [x] Predecessor task and evidence were inspected.
- [x] Focused tests and compile check passed.
- [x] Predecessor reports parsed and agreed on counts.
- [x] Check reports and evidence were written.
- [ ] Commit and post-commit validation.

## Recovery

If resumed, inspect `status.yaml`, rerun the validation commands above, and do
not continue if unexpected dirty state or error/blocker findings appear.

## Retrospective

The check preserved the predecessor warning debt and did not repair or
regenerate any inspected source or projection surface.
