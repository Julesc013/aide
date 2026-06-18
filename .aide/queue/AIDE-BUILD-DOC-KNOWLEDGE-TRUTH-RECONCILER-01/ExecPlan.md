# ExecPlan: AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

## Objective

Build a deterministic, report-only Track B observer that compares selected
canonical and explanatory AIDE surfaces and emits GovernanceFinding report
records for documentation, OKF, queue, protocol, evidence, generated report,
context, and interop projection drift.

## Scope

Allowed changes are limited to:

- the task packet and task-local evidence;
- minimal queue index registration;
- `core/reconciler/doc_knowledge_truth.py`;
- `core/reconciler/tests/test_doc_knowledge_truth.py`;
- `core/reconciler/__init__.py`;
- self-management reconciler reports.

## Non-Goals

No documentation repair, OKF regeneration, generated-output ledger, formal
GovernanceFinding schema, CLI command, file move, rename, reference rewrite,
migration apply, runtime/provider/network/GitHub/branch/release behavior, or
target-repo mutation is authorized.

## Plan

1. Confirm accepted predecessor and live queue truth.
2. Implement a small deterministic observer module with explicit comparison
   rules and report-convention GovernanceFinding records.
3. Add focused standard-library tests around finding shape, report generation,
   and non-capability boundaries.
4. Generate JSON and Markdown reports.
5. Write task evidence, run validation, and stop at `needs_review`.

## Verification

- `py -3 -m unittest core.reconciler.tests.test_doc_knowledge_truth`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- report JSON parse and Markdown/JSON finding agreement checks
- task inspect and task evidence checks
- git whitespace checks
