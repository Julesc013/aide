# Validation Results

Executed so far:

- `py -3 .aide/queue/AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01/evidence/check_execution_host_contract.py`: PASS, result `PASS_WITH_WARNINGS`, material findings `0`.
- Direct `py -3 .aide/scripts/aide_lite.py execution-host status`: PASS_WITH_WARNINGS.
- Direct `py -3 .aide/scripts/aide_lite.py execution-host project --source contract-projection`: PASS_WITH_WARNINGS.
- Direct `py -3 .aide/scripts/aide_lite.py execution-host validate`: PASS_WITH_WARNINGS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_execution_host_contract.py`: PASS, 14 tests.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01`: PASS, classification `complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01`: PASS, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- Check reports and non-script evidence local absolute path scan: PASS, no matches.
- Check reports and non-script evidence secret-like scan: PASS, no matches.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS after check commit.
