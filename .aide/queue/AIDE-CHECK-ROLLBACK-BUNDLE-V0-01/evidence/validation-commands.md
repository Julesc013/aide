# Validation Commands

Core RollbackBundle validation:

- `py -3 -m py_compile core\protocol\rollback_bundle.py .aide\scripts\tests\test_aide_rollback_bundle_v0.py .aide\scripts\aide_lite.py`
- `py -3 -m unittest discover -s .aide\scripts\tests -p "test_aide_rollback_bundle_v0.py"`
- `py -3 .aide\scripts\aide_lite.py rollback-bundle status`
- `py -3 .aide\scripts\aide_lite.py rollback-bundle project`
- `py -3 .aide\scripts\aide_lite.py rollback-bundle validate`

Predecessor regression validation:

- `py -3 .aide\scripts\aide_lite.py distribution-manifest status`
- `py -3 .aide\scripts\aide_lite.py distribution-manifest project`
- `py -3 .aide\scripts\aide_lite.py distribution-manifest validate`
- `py -3 .aide\scripts\aide_lite.py project-lock status`
- `py -3 .aide\scripts\aide_lite.py project-lock project`
- `py -3 .aide\scripts\aide_lite.py project-lock validate`
- `py -3 .aide\scripts\aide_lite.py ownership-ledger status`
- `py -3 .aide\scripts\aide_lite.py ownership-ledger project`
- `py -3 .aide\scripts\aide_lite.py ownership-ledger validate`
- `py -3 .aide\scripts\aide_lite.py ownership-ledger migrate-q43`
- `py -3 .aide\scripts\aide_lite.py install-record status`
- `py -3 .aide\scripts\aide_lite.py install-record project`
- `py -3 .aide\scripts\aide_lite.py install-record validate`
- `py -3 .aide\scripts\aide_lite.py migration-record status`
- `py -3 .aide\scripts\aide_lite.py migration-record project`
- `py -3 .aide\scripts\aide_lite.py migration-record validate`
- `py -3 .aide\scripts\aide_lite.py update-plan status`
- `py -3 .aide\scripts\aide_lite.py update-plan project`
- `py -3 .aide\scripts\aide_lite.py update-plan validate`

Boundary and global validation:

- `py -3 .aide\scripts\aide_lite.py install validate`
- `py -3 .aide\scripts\aide_lite.py repair validate`
- `py -3 .aide\scripts\aide_lite.py upgrade validate`
- `py -3 .aide\scripts\aide_lite.py rollback validate`
- `py -3 .aide\scripts\aide_lite.py uninstall validate`
- `py -3 .aide\scripts\aide_lite.py release validate`
- `py -3 .aide\scripts\aide_lite.py release draft-validate`
- `py -3 .aide\scripts\aide_lite.py validate`

Task, hygiene, and Git validation:

- `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-ROLLBACK-BUNDLE-V0-01`
- `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-ROLLBACK-BUNDLE-V0-01`
- `py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-CHECK-ROLLBACK-BUNDLE-V0-01`
- `py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-CHECK-ROLLBACK-BUNDLE-V0-01`
- Path, credential-like, and source-output misuse scans over RollbackBundle reports and task evidence.
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide\scripts\aide_lite.py commit check --latest`
