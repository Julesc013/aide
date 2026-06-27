# Validation Results

Result:

- check result: `PASS_WITH_WARNINGS`
- material_finding_count: `0`
- missing_evidence: `0`
- recommended_next_task: `AIDE-ACCEPT-UPDATE-PLAN-V1-01`

Executed validation:

- `compileall`: `PASS`
- focused UpdatePlan tests: `PASS`, 7 tests
- `update-plan status`: `PASS_WITH_WARNINGS`
- `update-plan project`: `PASS_WITH_WARNINGS`
- `update-plan validate`: `PASS_WITH_WARNINGS`, `error_count: 0`
- DistributionManifest status/project/validate: `PASS_WITH_WARNINGS`
- ProjectLock status/project/validate: `PASS_WITH_WARNINGS`
- OwnershipLedger status/project/validate/migrate-q43: `PASS_WITH_WARNINGS`
- InstallRecord status/project/validate: `PASS_WITH_WARNINGS`
- MigrationRecord status/project/validate: `PASS_WITH_WARNINGS`
- Q43 install validator: `PASS`
- Q44 repair validator: `PASS`
- Q45 upgrade validator: `PASS`
- Q46 rollback validator: `PASS`
- Q46 uninstall validator: `PASS`
- Q47 release validator: `PASS`, no publish, no tag, no GitHub Release, no upload
- Q48 release draft validator: `PASS`, no publish, no tag, no GitHub Release, no upload, no network API call
- Broad AIDE validation: `PASS`
- Source task inspect: `PASS`, `missing_evidence: 0`
- Source task evidence: `PASS`, no missing evidence
- Independent semantic probe: `PASS`
- JSON report/schema parsing: `PASS`

Environment warning:

- Direct standalone PyYAML parsing remains unavailable because `yaml` is not installed in the active Python environment. AIDE-native task inspect/evidence and broad validation exercised queue YAML successfully, so this is not material for the check.
