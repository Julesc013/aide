# Validation Results

Final validation results:

| Command | Result |
| --- | --- |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | PASS |
| `py -3 .aide/scripts/tests/test_aide_distribution_product_status_projection.py` | PASS, 1 test |
| `py -3 .aide/scripts/aide_lite.py distribution-product status` | PASS_WITH_WARNINGS, projection routes to check task and readiness remains false |
| JSON parse and required-key check | PASS |
| Markdown heading check | PASS |
| `py -3 .aide/scripts/aide_lite.py distribution-apply status` | PASS_WITH_WARNINGS |
| `py -3 .aide/scripts/aide_lite.py distribution-apply plan` | PASS_WITH_WARNINGS |
| `py -3 .aide/scripts/aide_lite.py distribution-apply verify` | PASS_WITH_WARNINGS, material findings 0, missing evidence 0 |
| `py -3 .aide/scripts/aide_lite.py install validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py upgrade validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py rollback validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py uninstall validate` | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py release validate` | PASS, no_publish true |
| `py -3 .aide/scripts/aide_lite.py release draft-validate` | PASS, no_publish true |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01` | PASS, missing evidence 0 |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01` | PASS, missing none |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01` | PASS, missing evidence 0 |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01` | PASS, missing none |
| path safety scan | PASS, intended paths only |
| credential/secret-like added-line scan | PASS, no matches |
| source-output added-line scan | PASS, no matches |
| overclaim scan | PASS, no false readiness or apply claims |
| `git diff --check` | PASS |
| `git diff --cached --check` | PASS |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS |

Post-commit note: the first `commit check --latest` run failed on commit-message formatting only. The commit message was amended to add required bullet content, explicit validation outcomes, a categorized changelog item, and AIDE trailers; the final commit-policy check passed.
