# Safety Scans

Final scans are run over:

- `.aide/reports/distribution-apply-engine-v0`
- `.aide/queue/AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-01`

Required scan classes:

- local absolute path scan
- local ignored-state directory scan
- credential-pattern scan
- source latest-output-as-target-truth scan
- git whitespace scan

Expected result: PASS. Exact final scan command results are recorded in the terminal transcript and summarized in `validation-results.md`.
