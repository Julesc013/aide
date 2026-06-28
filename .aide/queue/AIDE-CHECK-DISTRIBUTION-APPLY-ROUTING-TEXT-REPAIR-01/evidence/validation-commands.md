# Validation Commands

Commands for this independent check:

- `py -3 -m py_compile .aide/scripts/aide_lite.py`
- `py -3 -m py_compile .aide/scripts/tests/test_aide_distribution_apply_routing_text_repair.py`
- `py -3 .aide/scripts/tests/test_aide_distribution_apply_routing_text_repair.py`
- `py -3 .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py`
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
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01`
- `git diff --name-only -- .aide/fixtures/aide-self-consumer-fixture-v0`
- path safety scan
- credential/secret-like added-line scan
- source-output added-line scan
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
