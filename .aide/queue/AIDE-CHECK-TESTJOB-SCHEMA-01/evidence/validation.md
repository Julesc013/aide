# Validation

Result: PASS_WITH_WARNINGS.

Preflight and inspection:

- `git status --short --branch`: PASS, clean before check artifacts.
- `git rev-parse HEAD`: PASS, `017b7e639cd2fc48a5bfad8bf91e5665f0d56e9e`.
- `git show --stat --oneline --name-status HEAD`: PASS, TestJob build commit.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-TESTJOB-SCHEMA-01`: PASS.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-TESTJOB-SCHEMA-01`: PASS.

Structural and focused checks:

- `py -3 -m py_compile core/protocol/test_job.py`: PASS.
- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS.
- `py -3 -m json.tool .aide/protocol/aide-test-job.schema.json`: PASS.
- `py -3 -m json.tool .aide/reports/test-job/projection-report.json`: PASS.
- `py -3 -m json.tool .aide/reports/test-job/validation.json`: PASS.
- `json.tool` over `.aide/reports/test-job/projections/*.test-job.json`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_test_job_schema.py`: PASS, 29 tests.

CLI and compatibility:

- `py -3 .aide/scripts/aide_lite.py test-job status`: PASS.
- `py -3 .aide/scripts/aide_lite.py test-job project --source accepted-artifacts`: PASS, 9 projections, source reports not mutated.
- `py -3 .aide/scripts/aide_lite.py test-job validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py worker-run validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py workunit-queue validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py evidence-packet validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py contract-envelope validate`: PASS.

Boundary checks:

- Unsupported `test-job submit/run/retry/summarize` subcommands returned exit code 2: PASS.
- PowerShell validation boundary flag check over `.aide/reports/test-job/validation.json`: PASS.
- Corrected secret-shaped token scan: PASS.
- Corrected positive overclaim scan: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS, no additional dirty files left.
- `git diff --check` after restoring generated churn: PASS.

Corrected checks:

- Initial PowerShell scans used unsupported `Select-String -Recurse`; corrected file-walk scans passed.
- Initial `git diff --check` after TestJob report refresh found a generated blank line at EOF; out-of-scope generated report churn was restored and the final check passed.

Warnings:

- Full JSON Schema Draft 2020-12 validation remains deferred.
- TestJob remains metadata-only by design.
- `.aide/context/latest-task-packet.md` remains stale relative to live queue truth.
- The attached frozen plan supersedes the older build evidence's after-acceptance PatchTransaction note; after acceptance the next planned task is `AIDE-BUILD-REFERENCE-ID-SCHEME-01`.
