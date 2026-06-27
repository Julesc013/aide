# Validation Commands

Core RollbackBundle validation:

- `py -3 -m py_compile core\protocol\rollback_bundle.py .aide\scripts\tests\test_aide_rollback_bundle_v0.py .aide\scripts\aide_lite.py`
- `py -3 -m unittest discover -s .aide\scripts\tests -p "test_aide_rollback_bundle_v0.py"`
- `py -3 .aide\scripts\aide_lite.py rollback-bundle status`
- `py -3 .aide\scripts\aide_lite.py rollback-bundle project`
- `py -3 .aide\scripts\aide_lite.py rollback-bundle validate`

Predecessor regression validation:

- `py -3 .aide\scripts\aide_lite.py distribution-manifest validate`
- `py -3 .aide\scripts\aide_lite.py project-lock validate`
- `py -3 .aide\scripts\aide_lite.py ownership-ledger validate`
- `py -3 .aide\scripts\aide_lite.py ownership-ledger migrate-q43`
- `py -3 .aide\scripts\aide_lite.py install-record validate`
- `py -3 .aide\scripts\aide_lite.py migration-record validate`
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
- Path, secret-like, and source-output scan over `.aide/reports/rollback-bundle-v0` and `.aide/queue/AIDE-BUILD-ROLLBACK-BUNDLE-V0-01`
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide\scripts\aide_lite.py commit check --latest`

Transient command false starts recorded in `validation-results.md`:

- A dotted-module unittest invocation failed because `.aide` is not importable as a package path in that form; the supported unittest discovery command passed.
- One parallel `rollback-bundle project` run hit a Windows file-lock race while another RollbackBundle command was generating fixtures/reports; the sequential rerun passed.
- The first hygiene scan used an unsupported `Select-String -Recurse` option in this shell; the corrected `Get-ChildItem -Recurse | Select-String` scan completed.
