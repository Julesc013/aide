# Validation Results

Result: PASS

Commands run:

- PASS: JSON schema/report parse for the OwnershipLedger v1 schema and acceptance report.
- PASS: `py -3 -m compileall core/protocol .aide/scripts/tests`.
- PASS: `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_ownership_ledger_v1.py`.
- PASS: `py -3 .aide/scripts/aide_lite.py ownership-ledger status`.
- PASS: `py -3 .aide/scripts/aide_lite.py ownership-ledger project`.
- PASS: `py -3 .aide/scripts/aide_lite.py ownership-ledger validate`.
- PASS: `py -3 .aide/scripts/aide_lite.py ownership-ledger migrate-q43`.
- PASS: `py -3 .aide/scripts/aide_lite.py distribution-manifest validate`.
- PASS: `py -3 .aide/scripts/aide_lite.py project-lock validate`.
- PASS: Q43-Q48 no-apply/no-publish validators through `install validate`, `repair validate`, `upgrade validate`, `rollback validate`, `uninstall validate`, `release validate`, and `release draft-validate`.
- PASS: `task inspect` and `task evidence` for build, check, repair, repair-check, and acceptance tasks.
- PASS: `py -3 .aide/scripts/aide_lite.py validate`.
- PASS: strict changed-report/evidence scans for local absolute paths, secret-like material, and source-output misuse.
- PASS: `git diff --check`.
- PASS: `git diff --cached --check`.

Notes:

- The source-output misuse scan initially matched only the scan label in `validation-commands.md`; the label was narrowed and the scan was rerun.
