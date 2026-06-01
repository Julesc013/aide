# AIDE Full-Discovery Handoff

- status: WAITING_FOR_EXTERNAL_FULL_DISCOVERY
- mode: report_only
- reason: X-TEST-00 external full-discovery example
- commit: eb100b4e315dd0fa1da5eaeed7ab2116d0c991a1
- branch: main
- command_to_run_externally: `py -3 -m unittest discover -s .aide/scripts/tests`
- expected_summary_path: `.aide/tests/latest-full-discovery-summary.json`
- full_suite_executed: false
- target_test_execution: false
- provider_or_model_calls: none
- network_calls: none

## Resume

Attach or commit the compact summary artifact, then rerun `py -3 .aide/scripts/aide_lite.py test summary-validate --file <summary>`.
