# Validation Results

- PASS: independent trust check harness.
- PASS: focused trust contract tests, 11 tests.
- PASS_WITH_WARNINGS: `aide_lite.py trust validate`.
- PASS_WITH_WARNINGS: `aide_lite.py trust status`.
- PASS: `compileall core/protocol .aide/scripts/tests`.
- PASS: deterministic trust projection rerun, 14 report files unchanged byte-for-byte by SHA-256.
- PASS: broad `aide_lite.py validate`.

The independent harness recorded 12 assertions, zero material findings, and
recommended `AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01`.
