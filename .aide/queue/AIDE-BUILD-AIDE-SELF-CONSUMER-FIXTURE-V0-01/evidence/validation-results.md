# Validation Results

Final validation results:

| Command | Result |
| --- | --- |
| `py -3 -m py_compile .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py` | PASS |
| `py -3 .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py` | PASS, 7 tests |
| `py -3 .aide/scripts/aide_lite.py distribution-apply verify` | PASS_WITH_WARNINGS, material findings 0, missing evidence 0 |
| `py -3 .aide/scripts/aide_lite.py install validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py upgrade validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py rollback validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py uninstall validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py release validate` | PASS, no_publish true |
| `py -3 .aide/scripts/aide_lite.py release draft-validate` | PASS, no_publish true |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01` | PASS, evidence files 13, missing evidence 0 |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01` | PASS, missing none |
| credential-pattern scan | PASS, no matches |
| added-diff source-output misuse scan | PASS, no matches |
| new-surface source-output misuse scan | PASS, no matches after excluding scan documentation |
| `git diff --check` | PASS |
| `git diff --cached --check` | PASS |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS |

Notes:

- `distribution-apply verify` still prints build-era implementation status text that the self-consumer fixture is not started. This build does not edit DistributionApplyEngine status output; the new fixture task/report surfaces record the self-consumer fixture build.
- `commit check --latest` passed after the local commit was created.
