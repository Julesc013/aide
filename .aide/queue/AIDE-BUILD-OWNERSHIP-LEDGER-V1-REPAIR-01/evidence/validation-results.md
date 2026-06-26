# Validation Results

- `py -3 -m compileall core/protocol .aide/scripts/tests`: PASS
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_ownership_ledger_v1.py"`: PASS, 11 tests
- `py -3 .aide/scripts/aide_lite.py ownership-ledger status`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py ownership-ledger project`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py ownership-ledger validate`: PASS_WITH_WARNINGS, error_count 0
- `py -3 .aide/scripts/aide_lite.py ownership-ledger migrate-q43`: PASS_WITH_WARNINGS, error_count 0
- `py -3 .aide/scripts/aide_lite.py project-lock validate`: PASS_WITH_WARNINGS, error_count 0
- `py -3 .aide/scripts/aide_lite.py distribution-manifest validate`: PASS_WITH_WARNINGS, error_count 0
- `py -3 .aide/scripts/aide_lite.py validate`: PASS
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01`: PASS, classification complete, missing_evidence 0
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01`: PASS, missing list empty
- `git diff --check`: PASS
- `git diff --cached --check`: PASS before staging
- strict changed-diff local-path and secret-like scan: PASS
