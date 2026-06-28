# Validation Commands

Required validation commands:

- `py -3 -m py_compile .aide/scripts/aide_lite.py`
- `py -3 .aide/scripts/tests/test_aide_distribution_product_status_projection.py`
- `py -3 .aide/scripts/aide_lite.py distribution-product status`
- JSON parse and required-key check for `.aide/reports/distribution-product-status/current.json`
- Markdown heading check for `.aide/reports/distribution-product-status/current.md`
- `py -3 .aide/scripts/aide_lite.py distribution-apply status`
- `py -3 .aide/scripts/aide_lite.py distribution-apply plan`
- `py -3 .aide/scripts/aide_lite.py distribution-apply verify`
- `py -3 .aide/scripts/aide_lite.py install validate`
- `py -3 .aide/scripts/aide_lite.py upgrade validate`
- `py -3 .aide/scripts/aide_lite.py rollback validate`
- `py -3 .aide/scripts/aide_lite.py uninstall validate`
- `py -3 .aide/scripts/aide_lite.py release validate`
- `py -3 .aide/scripts/aide_lite.py release draft-validate`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`
- path safety scan
- credential/secret-like scan
- source-output scan
- overclaim scan
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
