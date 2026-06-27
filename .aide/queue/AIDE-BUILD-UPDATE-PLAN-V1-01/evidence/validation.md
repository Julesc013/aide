# Validation

Final validation result:

- result: `PASS_WITH_WARNINGS`
- material_finding_count: `0`
- missing_evidence: `0`
- recommended_next_task: `AIDE-CHECK-UPDATE-PLAN-V1-01`

Key checks:

- UpdatePlan schema and generated reports parse as JSON.
- UpdatePlan helper, tests, and CLI compile.
- Focused UpdatePlan unit tests pass.
- `update-plan status`, `project`, and `validate` pass with warnings.
- DistributionManifest, ProjectLock, OwnershipLedger, InstallRecord, and MigrationRecord regressions pass with warnings.
- Q43-Q48 no-apply/no-publish validators pass.
- Broad `aide_lite.py validate` passes.
- Task inspect/evidence reports `missing_evidence: 0`.

Direct PyYAML parsing was unavailable because PyYAML is not installed in this environment; task YAML was still exercised by AIDE task inspection and evidence commands.
