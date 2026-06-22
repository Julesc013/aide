# Validation Results

- PASS: `git diff --check`.
- PASS: `git diff --cached --check`.
- PASS: `git rev-parse 84a154c` resolved `84a154c2f03b304a987a9f017cc48a0b22c3f6d6`.
- PASS: `git show --no-patch --format=fuller 84a154c`.
- PASS: `py -3 -m compileall core\interop\dominium core\protocol .aide\scripts\tests`.
- PASS: seam unittest discovery ran 158 tests in 1288.197 seconds.
- PASS_WITH_WARNINGS: `dominium-seam status`.
- PASS: `dominium-seam snapshot`.
- PASS_WITH_WARNINGS: `dominium-seam project` after rerun with longer timeout.
- PASS_WITH_WARNINGS: `dominium-seam validate`.
- PASS: `dominium-seam diff`.
- PASS_WITH_WARNINGS: `dominium-seam demo`.
- REQUEST_CHANGES: independent Repair 03 check harness found 12 material assertions.
- PASS: task inspect/evidence for `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` reported `missing_evidence: 0`.
- PASS: task inspect/evidence for `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-03` reported `missing_evidence: 0`.
- PASS: broad `py -3 .aide\scripts\aide_lite.py validate`.
- PASS: strict credential-pattern scan found no credential-like material after excluding the command-log self-hit.
- PASS: `py -3 .aide\scripts\aide_lite.py commit check --latest`.
