# Validation

Validation commands run before writing this evidence:

- `git status --short --branch`: `## main...origin/main`
- `git merge-base --is-ancestor fca99236c2f933660de29b657dc181f1174dd719 HEAD`: pass
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`: complete, `missing_evidence: 0`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`: complete
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`: complete, `missing_evidence: 0`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`: complete
- direct independent drive-prefix probes: pass
- direct independent duplicate-normalization probes: pass
- temporary-workspace repeated projection comparison: pass
- unsupported apply/approve/execute/rollback probes: pass, failed closed
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_patch_transaction.py`: pass, 31 tests
- `py -3 .aide/scripts/aide_lite.py patch-transaction status`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py patch-transaction project`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py patch-transaction validate`: `PASS_WITH_WARNINGS`

Final validation matrix and commit-policy results are recorded after report
materialization and before commit.

Post-materialization validation:

- `git diff --check`: pass with the known CRLF notice for
  `.aide/queue/index.yaml`, no whitespace error.
- `git diff --cached --check`: pass before staging.
- `py -3 -m py_compile core/protocol/patch_transaction.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_patch_transaction.py`: pass.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_patch_transaction.py`: pass, 31 tests.
- `py -3 .aide/scripts/aide_lite.py reference-id validate`: `PASS_WITH_WARNINGS`.
- `py -3 .aide/scripts/aide_lite.py event-record validate`: `PASS_WITH_WARNINGS`.
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`: `PASS`.
- `py -3 .aide/scripts/aide_lite.py workunit validate`: `PASS`.
- `py -3 .aide/scripts/aide_lite.py worker-run validate`: `PASS`.
- `py -3 .aide/scripts/aide_lite.py test-job validate`: `PASS`.
- `py -3 .aide/scripts/aide_lite.py capability-manifest validate`: `PASS_WITH_WARNINGS`.
- `py -3 .aide/scripts/aide_lite.py conformance-profile validate`: `PASS_WITH_WARNINGS`.
- `py -3 .aide/scripts/aide_lite.py conformance-result validate`: `PASS_WITH_WARNINGS`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01`: complete, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01`: complete, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py validate`: `PASS`.
- JSON parsing for repair-check reports: pass.
- Secret-like value scan over changed files: 0 findings.
- Unrelated generated churn from predecessor validators was restored before final staging.
