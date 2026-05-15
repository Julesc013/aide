# Export Pack Audit

## Manifest Summary

- Pack path: `.aide/export/aide-lite-pack-v0/`
- Manifest: `.aide/export/aide-lite-pack-v0/manifest.yaml`
- Checksums: `.aide/export/aide-lite-pack-v0/checksums.json`
- Export report: `.aide/export/aide-lite-pack-v0/export-report.md`
- Latest export command summary: 629 included files, 632 checksum entries.

## Checksum Summary

`pack-status` result: PASS.

- `checksums_valid`: true
- `checksum_problems`: 0
- `boundary_violations`: 0
- `provenance_result`: `DIRTY_SOURCE_RECORDED`

The dirty-source provenance is expected because validation/export commands ran while QCHECK audit artifacts and generated validation outputs were present.

## Included Portable Surface Summary

The pack includes portable AIDE Lite support for:

- intent/workunit compilation
- repo intelligence
- quality reports
- refactor/root/tool dry-run models
- install/repair/upgrade/rollback/uninstall no-apply lifecycle models
- release bundle and release draft local commands
- policies, schemas, docs, tests, and golden tasks

## Excluded Generated/Source-State Summary

The pack is intended to exclude:

- `.aide.local/**`
- `.env`
- secrets
- raw prompt bodies
- raw response bodies
- source-generated current repo observations/plans/reports as target truth
- release bundle dist outputs as target truth
- GitHub release draft outputs as target truth

## Source-State Leakage Scan

Targeted scans found only policy, documentation, fixture, regex, and example strings. No actual provider credential, local state payload, raw prompt body, or raw response body was found.

Allowed examples include `.aide.local.example` and literal deny-pattern text in policies/tests.

## Target-Safety Verdict

PASS_WITH_WARNINGS.

The export pack is valid and checksum-backed. Use the safe import/preflight path. Do not manually copy the pack payload as an install substitute.
