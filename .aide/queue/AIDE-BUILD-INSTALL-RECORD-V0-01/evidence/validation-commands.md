# Validation Commands

Validation commands for this build task:

- `py -3 -m compileall core/protocol .aide/scripts/tests/test_aide_install_record_v0.py .aide/scripts/aide_lite.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_install_record_v0.py`
- `py -3 .aide/scripts/aide_lite.py install-record status`
- `py -3 .aide/scripts/aide_lite.py install-record project`
- `py -3 .aide/scripts/aide_lite.py install-record validate`
- `py -3 .aide/scripts/aide_lite.py distribution-manifest validate`
- `py -3 .aide/scripts/aide_lite.py project-lock validate`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger validate`
- Q43-Q48 no-apply/no-publish validators
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-INSTALL-RECORD-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-INSTALL-RECORD-V0-01`
- generated report/evidence scans for local paths, secret-like material, and source-output misuse
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
