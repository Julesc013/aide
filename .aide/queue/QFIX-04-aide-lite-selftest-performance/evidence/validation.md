# Validation

- `git diff --check`: PASS
  - Notes: Git reported CRLF-to-LF normalization warnings for touched test files; no whitespace errors.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS
- `py -3 .aide/scripts/aide_lite.py test`: PASS
- `py -3 .aide/scripts/aide_lite.py validate`: PASS
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS
  - Result: 117 tasks, 117 pass, 0 warn, 0 fail.
  - Generated eval reports were restored because they are outside this QFIX scope.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS
  - included_files: 555
  - checksum_count: 558
  - boundary_result: PASS
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS
  - checksums_valid: true
  - provenance_result: DIRTY_SOURCE_RECORDED
  - boundary_result: PASS
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS
  - Existing warning: `.aide/generated/manifest.yaml` source fingerprint is stale.
- `py -3 .aide/scripts/tests/test_aide_lite.py`: PASS
  - 16 tests in 103.773 seconds.
- `py -3 .aide/scripts/tests/test_golden_tasks.py`: PASS
  - 9 tests in 99.081 seconds after report-subset optimization.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS
  - 27 tests in 80.421 seconds.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS
  - 9 tests in 1.339 seconds.

## Invalid Commands

- `py -3 -m unittest .aide/scripts/tests/test_aide_lite.py`: invalid unittest module form for a path under a dot-prefixed directory; failed before loading tests.
- `py -3 -m unittest .aide/scripts/tests/test_golden_tasks.py`: invalid unittest module form for a path under a dot-prefixed directory; failed before loading tests.

The invalid invocations were rerun using direct Python file execution and passed.
