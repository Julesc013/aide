# Validation Results

Initial focused validation passed:

- Focused DistributionApplyEngine tests: `9` tests passed.
- `distribution-apply status`: `PASS_WITH_WARNINGS`, `scenario_count: 46`.
- `distribution-apply plan --scenario managed-file-update`: passed.
- `distribution-apply run --scenario managed-file-update --mode apply-temp`: `PASS_WITH_WARNINGS`, rollback verified, UpdateReceipt fixture output generated.
- `distribution-apply verify`: `PASS_WITH_WARNINGS`, `material_finding_count: 0`, `missing_evidence: 0`.
- Adversarial context-binding scenario runs: all refused with expected reason codes, no successful UpdateReceipt output, no real target/source apply.

Final validation receipts are recorded in this task packet and in `.aide/reports/distribution-apply-engine-v0-repair-01/validation-summary.json`.
