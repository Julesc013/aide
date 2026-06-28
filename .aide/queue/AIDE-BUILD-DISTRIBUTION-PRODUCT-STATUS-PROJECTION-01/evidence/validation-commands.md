# Validation Commands

Planned and run validation:

```text
py -3 -m py_compile .aide/scripts/aide_lite.py
py -3 -m py_compile .aide/scripts/tests/test_aide_distribution_product_status_projection.py
py -3 .aide/scripts/tests/test_aide_distribution_product_status_projection.py
py -3 .aide/scripts/aide_lite.py distribution-product status
py -3 -c "import json, pathlib; data=json.loads(pathlib.Path('.aide/reports/distribution-product-status/current.json').read_text(encoding='utf-8')); required=['projection','current','accepted','readiness','canaries','explicit_non_capabilities','warning_debt','recommended_next_tasks']; missing=[key for key in required if key not in data]; raise SystemExit(1 if missing else 0)"
py -3 -c "from pathlib import Path; text=Path('.aide/reports/distribution-product-status/current.md').read_text(encoding='utf-8'); required=['# Distribution Product Status','## Current gate','## Accepted capabilities and boundaries','## Fixture-only boundaries','## Explicit non-capabilities','## Readiness matrix','## Canary readiness','## Warning debt','## Latest validation','## Next recommended tasks','## Source refs']; missing=[heading for heading in required if heading not in text]; raise SystemExit(1 if missing else 0)"
py -3 .aide/scripts/aide_lite.py distribution-apply status
py -3 .aide/scripts/aide_lite.py distribution-apply plan
py -3 .aide/scripts/aide_lite.py distribution-apply verify
py -3 .aide/scripts/aide_lite.py install validate
py -3 .aide/scripts/aide_lite.py upgrade validate
py -3 .aide/scripts/aide_lite.py rollback validate
py -3 .aide/scripts/aide_lite.py uninstall validate
py -3 .aide/scripts/aide_lite.py release validate
py -3 .aide/scripts/aide_lite.py release draft-validate
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01
path safety scan
credential/secret-like scan
source-output scan
no-overclaim scan
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py commit check --latest
```
