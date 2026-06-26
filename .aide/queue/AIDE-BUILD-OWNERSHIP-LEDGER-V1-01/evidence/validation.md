# Validation

Initial validation passed:

- `py -3 -m py_compile core/protocol/ownership_ledger.py .aide/scripts/aide_lite.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_ownership_ledger_v1.py"`: `8` tests passed.
- `py -3 .aide/scripts/aide_lite.py ownership-ledger validate`: `PASS_WITH_WARNINGS`

Final validation after task materialization is recorded before commit.

Final validation passed:

- `py -3 .aide/scripts/aide_lite.py ownership-ledger status`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger project`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-OWNERSHIP-LEDGER-V1-01`: `missing_evidence: 0`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-OWNERSHIP-LEDGER-V1-01`: no missing evidence
- `py -3 .aide/scripts/aide_lite.py project-lock validate`: `PASS_WITH_WARNINGS`
- `py -3 .aide/scripts/aide_lite.py validate`: `PASS`
- `git diff --check`: pass
- `git diff --cached --check`: pass before staging
