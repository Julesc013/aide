# Validation

## Completed

- `py -3 -m json.tool .aide/protocol/aide-distribution-manifest-v1.schema.json > $null`: PASS
- `py -3 -m compileall core/protocol .aide/scripts/tests`: PASS
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_distribution_manifest_v1.py"`: PASS
- `py -3 .aide/scripts/aide_lite.py distribution-manifest status`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py distribution-manifest project`: PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py distribution-manifest validate`: PASS_WITH_WARNINGS, `error_count: 0`
- `git diff --check`: PASS after restoring unrelated generated churn
- `git diff --cached --check`: PASS

## Final Evidence

- Broad AIDE validation: PASS.
- Task inspect/evidence recheck: PASS with `missing_evidence: 0`.
- Local path scan: PASS.
- Secret-like scan: PASS.
- Full command receipts are recorded in `validation-results.json`.
