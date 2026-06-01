# Command Surface Evidence

Implemented and exercised report-only commands:

- `py -3 .aide/scripts/aide_lite.py test`
- `py -3 .aide/scripts/aide_lite.py test tiers`
- `py -3 .aide/scripts/aide_lite.py test tier-plan`
- `py -3 .aide/scripts/aide_lite.py test impact-plan --from HEAD`
- `py -3 .aide/scripts/aide_lite.py test summary-validate --file .aide/tests/examples/test-summary.example.json`
- `py -3 .aide/scripts/aide_lite.py test summary-validate --file .aide/tests/examples/test-summary.invalid-raw-log.json` exits non-zero as expected.
- `py -3 .aide/scripts/aide_lite.py test telemetry-status`
- `py -3 .aide/scripts/aide_lite.py test full-discovery-handoff --reason "..."`
- `py -3 .aide/scripts/aide_lite.py test slow-report-validate --file .aide/tests/examples/slow-test-report.example.json`

The legacy `test` command remains the AIDE Lite selftest alias.
