# Safety Scans

Safety scans over `.aide/reports/update-plan-v1` and `.aide/queue/AIDE-BUILD-UPDATE-PLAN-V1-01/evidence`:

- local absolute path scan: `PASS`
- secret-like assignment scan: `PASS`
- source latest-output-as-target-truth scan: `PASS`

The negative fixture corpus intentionally contains unsafe path examples and is not part of the report/evidence leak scan.
