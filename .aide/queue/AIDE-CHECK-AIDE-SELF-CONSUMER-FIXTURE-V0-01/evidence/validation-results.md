# Validation Results

Final validation results:

| Command | Result |
| --- | --- |
| `py -3 -m py_compile .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py` | PASS |
| `py -3 .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py` | PASS, 7 tests |
| structured fixture JSON review | PASS, 9 scenarios and required lifecycle proofs |
| canonical fixture hash preservation | PASS, before/after hashes match |
| `py -3 .aide/scripts/aide_lite.py distribution-apply status` | PASS_WITH_WARNINGS boundary status |
| `py -3 .aide/scripts/aide_lite.py distribution-apply plan --scenario managed-file-update` | PASS |
| `py -3 .aide/scripts/aide_lite.py distribution-apply run --scenario managed-file-update --mode apply-temp` | PASS, temp workspace only |
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
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-AIDE-SELF-CONSUMER-FIXTURE-V0-01` | PASS, evidence files 17, missing evidence 0 |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-AIDE-SELF-CONSUMER-FIXTURE-V0-01` | PASS, missing none |
| path-boundary scan | PASS, intended paths only |
| credential-pattern scan | PASS, no matches |
| source-output misuse scan | PASS, no matches |
| `git diff --check` | PASS |
| `git diff --cached --check` | PASS |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS |

Notes:

- `distribution-apply status` still reports build-era status text that the self-consumer fixture is not started; this check records that as warning debt because the self-consumer fixture is now represented by its own queue and report surfaces.
- The check did not modify the self-consumer fixture corpus, focused tests, or DistributionApplyEngine implementation.
