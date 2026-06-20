# Validation

Commands run:

- `git status --short --branch`: PASS, AIDE branch `main`, only authorized check-task/report/index/log files changed.
- `git diff --check`: PASS, exit 0. Git reported CRLF normalization warnings for existing text files.
- `git diff --cached --check`: PASS, no staged whitespace errors.
- `py -3 -m py_compile .aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01/evidence/tools/check_dominium_seam_independent.py`: PASS.
- `py -3 .aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01/evidence/tools/check_dominium_seam_independent.py`: PASS as a completed check run; result inside report is `REQUEST_CHANGES` with 18 material findings.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`: PASS, complete, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`: PASS, `missing:` empty.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01`: initially PARTIAL before this file existed, expected `missing_evidence: 1` for `validation.md`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01`: initially reported missing `validation.md`; rerun required after this file is written.
- `py -3 -m unittest .aide.scripts.tests.test_aide_dominium_readonly_seam`: COMMAND ERROR, invalid unittest module invocation produced `ValueError: Empty module name`; not a seam test failure.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_dominium_readonly_seam.py`: PASS, 108 tests.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- JSON parsing for check report, independent check results, negative results, source-tree hashes, and evidence manifest: PASS.
- `rg -n --hidden -S "(sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN (RSA |OPENSSH |EC |DSA |)?PRIVATE KEY-----|AKIA[0-9A-Z]{16})" .aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01 .aide/reports/dominium-readonly-seam-v0-check`: PASS, no matches; `rg` exited 1 because no matches were found.
- `git -C C:\Projects\Dominium\dominium status --short --branch`: PASS, unchanged `## main...origin/main [behind 24]`.

Independent check result:

- `REQUEST_CHANGES`
- material findings: `18`
- warnings: `1`
- recommended next task: `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01`

No production seam files, build reports, build fixtures, interop outputs, accepted predecessor artifacts, or Dominium files were modified.
