# Validation Results

## Result

`PASS_WITH_WARNINGS`

## Observed Results

- Component task inspect/evidence aggregate: PASS, all `missing_evidence: 0`.
- Barrier JSON and findings JSON parse.
- Barrier report records `b1_complete: true`.
- Barrier report records `track_b_pause_authorized: true`.
- Barrier report records `track_a_resume_authorized: true`.
- Barrier report records `blocking_findings: 0` and `error_findings: 0`.
- Live next Track A task resolved as `AIDE-ACCEPT-CAPABILITY-MANIFEST-01`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-TRACK-B-B1-BARRIER-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-TRACK-B-B1-BARRIER-01`: PASS, no missing evidence.
- `git diff --check`: PASS_WITH_WARNING, known `.aide/queue/index.yaml` CRLF warning only.

## Post-Commit And End-Of-Wave Results

- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~5..HEAD`: PASS for all five wave commits.
- `py -3 -m unittest core.reconciler.tests.test_doc_knowledge_truth core.reconciler.tests.test_generated_output_ledger core.reconciler.tests.test_report_index`: PASS, 10 tests.
- `py -3 -m py_compile core/reconciler/doc_knowledge_truth.py core/reconciler/generated_output_ledger.py core/reconciler/report_index.py core/reconciler/tests/test_doc_knowledge_truth.py core/reconciler/tests/test_generated_output_ledger.py core/reconciler/tests/test_report_index.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- Task inspect/evidence for all five wave tasks: PASS, all `missing_evidence: 0`.
- Markdown/JSON agreement for all five wave reports: PASS.
- GeneratedOutputLedger baseline replay at `af3156a`: PASS, 1,381 candidates.
- ReportIndex baseline replay at `bdfa1b7`: PASS, 479 reports and 70 ambiguity records.
- Current-head self-reference stability checks for GeneratedOutputLedger and ReportIndex: PASS.
- Final `git diff --check`: PASS.
- Final `git status --short --branch`: clean, `main...origin/main [ahead 5]`.
