# Validation Commands

- `py -3 .aide/scripts/aide_lite.py migration-record validate`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_migration_record_v0.py`
- report/evidence local path scan
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-MIGRATION-RECORD-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-MIGRATION-RECORD-V0-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-MIGRATION-RECORD-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-MIGRATION-RECORD-V0-01`
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
