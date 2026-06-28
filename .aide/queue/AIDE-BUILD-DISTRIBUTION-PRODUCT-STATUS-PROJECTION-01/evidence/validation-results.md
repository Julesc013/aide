# Validation Results

Final validation results:

| Command | Result |
| --- | --- |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | PASS |
| `py -3 -m py_compile .aide/scripts/tests/test_aide_distribution_product_status_projection.py` | PASS |
| `py -3 .aide/scripts/tests/test_aide_distribution_product_status_projection.py` | PASS, 1 test |
| `py -3 .aide/scripts/aide_lite.py distribution-product status` | PASS_WITH_WARNINGS |
| JSON parse and required-key check | PASS |
| Markdown existence and heading check | PASS |
| `py -3 .aide/scripts/aide_lite.py distribution-apply status` | PASS_WITH_WARNINGS |
| `py -3 .aide/scripts/aide_lite.py distribution-apply plan` | PASS_WITH_WARNINGS when rerun serially |
| `py -3 .aide/scripts/aide_lite.py distribution-apply verify` | PASS_WITH_WARNINGS |
| Q43-Q48 no-apply/no-publish validators | PASS |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS |
| task inspect/evidence | PASS, `missing_evidence: 0` |
| path safety scan | PASS |
| credential/secret-like scan | PASS, targeted added-line and untracked-file scan |
| source-output scan | PASS |
| no-overclaim scan | PASS |
| `git diff --check` | PASS |
| `git diff --cached --check` | PASS |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS |
