# Validation Results

Executed so far:

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_execution_host_contract.py`: PASS, 14 tests.
- `py -3 .aide/scripts/aide_lite.py execution-host status`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py execution-host project --source contract-projection`: PASS_WITH_WARNINGS, six projections written.
- `py -3 .aide/scripts/aide_lite.py execution-host validate`: PASS_WITH_WARNINGS.
- `py -3 -m compileall core/protocol .aide/scripts/tests`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_registered_process_provider.py`: PASS, 8 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_worker_run_schema.py`: PASS, 23 tests.
- initial `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01`: PARTIAL, missing `validation.md` and `remaining-risks.md`.
- initial `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01`: PARTIAL, missing `validation.md` and `remaining-risks.md`.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- final `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01`: PASS, classification `complete`, `missing_evidence: 0`.
- final `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01`: PASS, no missing evidence.
- new execution-host implementation/report/task local absolute path scan: PASS, no matches.
- new execution-host implementation/report/task secret-like assignment scan: PASS, no matches.
- added root-log/script/protocol line local absolute path scan: PASS, no matches.
- added root-log/script/protocol line secret-like assignment scan: PASS, no matches.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS after build commit.
