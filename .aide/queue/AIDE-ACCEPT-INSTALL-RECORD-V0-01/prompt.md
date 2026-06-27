# Prompt: AIDE-ACCEPT-INSTALL-RECORD-V0-01

Create and process `AIDE-ACCEPT-INSTALL-RECORD-V0-01`.

Repo truth outranks this prompt. Inspect the live checkout before acting.

Authority:

- Acceptance only.
- Do not repair InstallRecord implementation.
- Do not start MigrationRecord implementation.
- Do not perform or authorize install/update/migration/rollback/uninstall apply.
- Do not mutate target repos, create release archives, publish releases, create tags, upload artifacts, create GitHub Releases, call provider/model/network services, or start runtime/canary work.

Acceptance objectives:

1. Confirm InstallRecord build and check tasks are complete.
2. Confirm the independent check result is `PASS` or `PASS_WITH_WARNINGS`.
3. Confirm `material_finding_count: 0`.
4. Confirm `missing_evidence: 0`.
5. Accept only `install_record_v0` as a no-apply install-state record protocol/helper/projection/validation capability.
6. Record accepted contract, warnings, explicit non-capabilities, and downstream-use boundary.
7. Recommend exactly `AIDE-BUILD-MIGRATION-RECORD-V0-01`.
