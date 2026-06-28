# Validation Results

Final validation results:

| Command | Result |
| --- | --- |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | PASS |
| `py -3 -m py_compile .aide/scripts/tests/test_aide_distribution_apply_routing_text_repair.py` | PASS |
| `py -3 .aide/scripts/tests/test_aide_distribution_apply_routing_text_repair.py` | PASS, 1 test |
| `py -3 .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py` | PASS, 7 tests |
| `py -3 .aide/scripts/aide_lite.py distribution-apply status` | PASS_WITH_WARNINGS, routes to product-status projection |
| `py -3 .aide/scripts/aide_lite.py distribution-apply plan` | PASS_WITH_WARNINGS, default scenario `managed-file-update`, routes to product-status projection |
| `py -3 .aide/scripts/aide_lite.py distribution-apply verify` | PASS_WITH_WARNINGS, material findings 0, missing evidence 0 |
| `py -3 .aide/scripts/aide_lite.py install validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py upgrade validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py rollback validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py uninstall validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py release validate` | PASS, no_publish true |
| `py -3 .aide/scripts/aide_lite.py release draft-validate` | PASS, no_publish true |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01` | PASS, evidence files 12, missing evidence 0 |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01` | PASS, missing none |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01` | PASS, evidence files 14, missing evidence 0 |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01` | PASS, missing none |
| `git diff --name-only -- .aide/fixtures/aide-self-consumer-fixture-v0` | PASS, no changed paths |
| path safety scan | PASS, intended paths only |
| credential/secret-like added-line scan | PASS, no matches |
| source-output added-line scan | PASS, no matches |
| overclaim scan | PASS, no false readiness or apply claims |
| `git diff --check` | PASS |
| `git diff --cached --check` | PASS |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS |
