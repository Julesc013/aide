# Validation Commands

The independent check harness ran:

- `py -3 -m compileall core/protocol .aide/scripts/tests`
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_ownership_ledger_v1.py"`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger status`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger project`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger validate`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger migrate-q43`
- `py -3 .aide/scripts/aide_lite.py project-lock validate`
- `py -3 .aide/scripts/aide_lite.py distribution-manifest validate`
- `py -3 .aide/scripts/aide_lite.py validate`

Additional outer validation is recorded in `validation.md`.
