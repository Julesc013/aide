# Validation Commands

Planned validation:

- `py -3 -c "import json, pathlib; ..."`
- `py -3 -m compileall core/protocol .aide/scripts/tests`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_ownership_ledger_v1.py`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger status`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger project`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger validate`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger migrate-q43`
- `py -3 .aide/scripts/aide_lite.py distribution-manifest validate`
- `py -3 .aide/scripts/aide_lite.py project-lock validate`
- `py -3 .aide/scripts/aide_lite.py install validate`
- `py -3 .aide/scripts/aide_lite.py repair validate`
- `py -3 .aide/scripts/aide_lite.py upgrade validate`
- `py -3 .aide/scripts/aide_lite.py rollback validate`
- `py -3 .aide/scripts/aide_lite.py uninstall validate`
- `py -3 .aide/scripts/aide_lite.py release validate`
- `py -3 .aide/scripts/aide_lite.py release draft-validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id <source-or-acceptance-task>`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id <source-or-acceptance-task>`
- `py -3 .aide/scripts/aide_lite.py validate`
- strict local path, secret-like, and source-output misuse scans over changed reports/evidence
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
