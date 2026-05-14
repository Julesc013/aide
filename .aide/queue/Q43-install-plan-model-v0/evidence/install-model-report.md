# Install Model Report

## Policy And Schema Summary

- Install policy: `.aide/policies/install.yaml`
- Preservation policy: `.aide/policies/install-preservation.yaml`
- Ownership policy: `.aide/policies/install-ownership.yaml`
- Conflict policy: `.aide/policies/install-conflicts.yaml`
- Migration policy: `.aide/policies/install-migrations.yaml`
- Verification policy: `.aide/policies/install-verification.yaml`
- Schemas: `.aide/install/*.schema.json`

## Command Summary

Q43 adds the AIDE Lite `install` command family:

- `install observe`
- `install plan`
- `install dry-run`
- `install validate`
- `install status`
- `install explain PATH`
- `install ownership`
- `install conflicts`

All commands are deterministic and local. They do not call providers, models, or network services.

## Generated Artifacts

- `.aide/install/latest-install-observation.json`
- `.aide/install/latest-install-observation.md`
- `.aide/install/latest-install-plan.json`
- `.aide/install/latest-install-plan.md`
- `.aide/install/latest-install-dry-run.json`
- `.aide/install/latest-install-dry-run.md`
- `.aide/install/latest-ownership-ledger.example.json`
- `.aide/install/latest-conflict-report.json`
- `.aide/install/latest-conflict-report.md`
- `.aide/install/latest-preservation-report.md`
- `.aide/install/latest-verification-plan.md`

## Latest Counts

- observed files: 2007
- target-specific files: 795
- install plan operations: 462
- preserved paths: 1055
- conflicts: 458
- blocking conflicts: 0
- mandatory migration candidates: 0

## No-Apply Guarantee

- `no_apply: true`
- `apply_allowed: false` for install operations
- `overwrite_allowed: false` by default
- `target_mutation: false`
- no install apply command exists in Q43
