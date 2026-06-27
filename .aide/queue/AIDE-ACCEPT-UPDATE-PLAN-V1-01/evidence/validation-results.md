# Validation Results

Result:

- acceptance result: `ACCEPTED_WITH_WARNINGS`
- accepted capability: `update_plan_v1`
- material_finding_count: `0`
- missing_evidence: `0`
- recommended next task: `AIDE-BUILD-ROLLBACK-BUNDLE-V0-01`

Validation summary:

- Source build task inspect/evidence: `PASS`, `missing_evidence: 0`.
- Source check task inspect/evidence: `PASS`, `missing_evidence: 0`.
- Focused UpdatePlan compile and tests: `PASS`.
- `update-plan status/project/validate`: `PASS_WITH_WARNINGS`.
- Broad AIDE validation: `PASS`.
- Acceptance task inspect/evidence: `PASS`, `missing_evidence: 0`.
- Acceptance report/evidence safety scans: `PASS`.
- Diff and staged diff checks: `PASS`.

Accepted warnings:

- UpdatePlan v1 remains no-apply metadata and does not update targets.
- Same-session check independence is reduced.
- Standalone PyYAML is unavailable, but AIDE-native queue validation passed.
- Live unknown and never-touch conflicts are fail-closed warning-class conflicts.
