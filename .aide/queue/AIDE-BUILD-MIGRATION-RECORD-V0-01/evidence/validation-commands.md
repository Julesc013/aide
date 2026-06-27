# Validation Commands

- `py -3 -m compileall -q core/protocol .aide/scripts/tests/test_aide_migration_record_v0.py .aide/scripts/aide_lite.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_migration_record_v0.py`
- `py -3 .aide/scripts/aide_lite.py migration-record status`
- `py -3 .aide/scripts/aide_lite.py migration-record project`
- `py -3 .aide/scripts/aide_lite.py migration-record validate`
- predecessor regression validation
- Q43-Q48 no-apply/no-publish validators
- broad `py -3 .aide/scripts/aide_lite.py validate`
- task inspect/evidence
- changed report/evidence safety scans
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
