# Validation Commands

- `py -3 -m compileall -q core/protocol .aide/scripts/tests/test_aide_migration_record_v0.py .aide/scripts/aide_lite.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_migration_record_v0.py`
- `py -3 .aide/scripts/aide_lite.py migration-record project`
- `py -3 .aide/scripts/aide_lite.py migration-record validate`
- corrected local absolute path scan
- broad validation and no-apply/no-publish validators before commit
- task inspect/evidence
- diff checks
- commit policy check
