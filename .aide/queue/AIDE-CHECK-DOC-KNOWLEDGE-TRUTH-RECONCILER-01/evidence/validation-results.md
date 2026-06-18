# Validation Results

## Result

`PASS_WITH_WARNINGS`

## Commands Run

- `git status --short --branch`
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`
- `py -3 -m unittest core.reconciler.tests.test_doc_knowledge_truth`
- `py -3 -m py_compile core/reconciler/doc_knowledge_truth.py core/reconciler/tests/test_doc_knowledge_truth.py`
- `validate_doc_knowledge_truth_reports('.')`
- JSON parse for predecessor and check reports.
- Markdown/JSON finding agreement checks.

## Observed Results

- Preflight worktree was clean.
- `doctor` passed.
- `validate` passed.
- Predecessor task inspect reported `classification: complete` and
  `missing_evidence: 0`.
- Predecessor task evidence listed six files and no missing entries.
- Focused tests passed: 3 tests.
- Python compile check passed.
- Predecessor report validation returned `PASS_WITH_WARNINGS`.
- Recorded predecessor counts and current mechanical counts matched:
  900 sources and 12 findings.

## Warnings

- Review independence is reduced because prior build context is available in
  this thread.
- The predecessor warning findings remain unresolved by design.
