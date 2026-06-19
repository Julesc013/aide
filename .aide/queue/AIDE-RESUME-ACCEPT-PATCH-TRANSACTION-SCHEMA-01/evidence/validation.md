# Validation

Validation evidence for this resume acceptance:

- `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01` inspected as complete with
  `missing_evidence: 0`.
- Repair-check reports parse and recommend this resume task.
- Focused PatchTransaction tests passed during repair-check validation:
  31 tests.
- PatchTransaction `status`, `project`, and `validate` returned
  `PASS_WITH_WARNINGS` during repair-check validation.
- Broad AIDE validation passed during repair-check validation.

Final task inspect/evidence checks, Git diff checks, JSON parsing, secret-like
scan, broad validation, and commit-policy validation are run before commit.

Final pre-commit validation:

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01`: complete, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01`: complete, no missing evidence.
- `git diff --check`: pass with the known CRLF notice for `.aide/queue/index.yaml`, no whitespace error.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_patch_transaction.py`: pass, 31 tests.
- `py -3 .aide/scripts/aide_lite.py patch-transaction status`: `PASS_WITH_WARNINGS`.
- `py -3 .aide/scripts/aide_lite.py patch-transaction validate`: `PASS_WITH_WARNINGS`.
- `py -3 .aide/scripts/aide_lite.py validate`: `PASS`.
- JSON parsing for resume acceptance reports: pass.
- Secret-like value scan over changed files: 0 findings.
