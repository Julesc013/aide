# Validation Commands

Commands and checks for this task:

- `py -3 -m py_compile .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py`
- `py -3 .aide/scripts/tests/test_aide_self_consumer_fixture_v0.py`
- structured fixture JSON review
- canonical fixture hash preservation before and after `distribution-apply plan/run/verify`
- `py -3 .aide/scripts/aide_lite.py distribution-apply status`
- `py -3 .aide/scripts/aide_lite.py distribution-apply plan --scenario managed-file-update`
- `py -3 .aide/scripts/aide_lite.py distribution-apply run --scenario managed-file-update --mode apply-temp`
- `py -3 .aide/scripts/aide_lite.py distribution-apply verify`
- `py -3 .aide/scripts/aide_lite.py install validate`
- `py -3 .aide/scripts/aide_lite.py upgrade validate`
- `py -3 .aide/scripts/aide_lite.py rollback validate`
- `py -3 .aide/scripts/aide_lite.py uninstall validate`
- `py -3 .aide/scripts/aide_lite.py release validate`
- `py -3 .aide/scripts/aide_lite.py release draft-validate`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-AIDE-SELF-CONSUMER-FIXTURE-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-AIDE-SELF-CONSUMER-FIXTURE-V0-01`
- path and credential-pattern scans
- source-output misuse scan
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
