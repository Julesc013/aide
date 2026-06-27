# Validation Commands

- `py -3 -c "import json; ..."`
- `py -3 -m compileall -q core/protocol .aide/scripts/tests/test_aide_install_record_v0.py .aide/scripts/aide_lite.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_install_record_v0.py`
- `py -3 .aide/scripts/aide_lite.py install-record status`
- `py -3 .aide/scripts/aide_lite.py install-record project`
- `py -3 .aide/scripts/aide_lite.py install-record validate`
- `py -3 .aide/scripts/aide_lite.py distribution-manifest validate`
- `py -3 .aide/scripts/aide_lite.py project-lock validate`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger validate`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger migrate-q43`
- Q43-Q48 no-apply/no-publish validators
- `py -3 .aide/scripts/aide_lite.py validate`
- task inspect/evidence for build, check, and acceptance tasks
- changed report/evidence safety scans
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
