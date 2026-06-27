# Validation Commands

Ran:

- `py -3 -c "import json, pathlib; json.loads(pathlib.Path(r'.aide/protocol/aide-update-receipt-v0.schema.json').read_text(encoding='utf-8')); print('schema_parse_ok')"`
- `py -3 -m py_compile core/protocol/update_receipt.py .aide/scripts/tests/test_aide_update_receipt_v0.py .aide/scripts/aide_lite.py`
- `py -3 -m compileall -q core .aide/scripts`
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_update_receipt_v0.py"`
- `py -3 .aide/scripts/aide_lite.py update-receipt status`
- `py -3 .aide/scripts/aide_lite.py update-receipt project`
- `py -3 .aide/scripts/aide_lite.py update-receipt validate`
- predecessor `status`, `project`, and `validate` commands for DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, MigrationRecord, UpdatePlan, and RollbackBundle
- `py -3 .aide/scripts/aide_lite.py ownership-ledger migrate-q43`
- `py -3 .aide/scripts/aide_lite.py install validate`
- `py -3 .aide/scripts/aide_lite.py repair validate`
- `py -3 .aide/scripts/aide_lite.py upgrade validate`
- `py -3 .aide/scripts/aide_lite.py rollback validate`
- `py -3 .aide/scripts/aide_lite.py uninstall validate`
- `py -3 .aide/scripts/aide_lite.py release validate`
- `py -3 .aide/scripts/aide_lite.py release publication-boundary`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-UPDATE-RECEIPT-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-UPDATE-RECEIPT-V0-01`
- coverage, path, secret-like, source-output, and downstream-start scans
- `git diff --check`
- `git diff --cached --check`

Commit validation is recorded after the check commit is created.
