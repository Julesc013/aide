# Fixture Inventory

## Roots

- Fixture root: `.aide/examples/apply/lifecycle-fixtures/`
- Fixture reports root: `.aide/reports/lifecycle-fixtures/`

## Source Pack Files

- `source-pack/manifest.json`
- `source-pack/files/generated-file.md`
- `source-pack/files/managed-section-source.md`
- `source-pack/files/upgrade-v1.md`
- `source-pack/files/upgrade-v2.md`
- `source-pack/files/uninstall-owned.md`

## Target Baselines

- `target/clean-empty/`
- `target/existing-manual-file/`
- `target/existing-managed-section/`
- `target/upgrade-v1-installed/`
- `target/drifted-managed-section/`
- `target/missing-marker/`
- `target/malformed-marker/`
- `target/duplicate-marker/`
- `target/nested-marker/`
- `target/uninstall-owned-and-manual/`
- `target/protected-path-attempt/`
- `target/path-traversal-attempt/`
- `target/broad-delete-attempt/`

## Expected States

- `expected/install-clean/`
- `expected/install-existing-manual-preserved/`
- `expected/install-managed-section/`
- `expected/upgrade-v2/`
- `expected/upgrade-manual-preserved/`
- `expected/drift-detected/`
- `expected/repair-plan-missing-marker/`
- `expected/repair-plan-malformed-marker/`
- `expected/rollback-record-generated/`
- `expected/uninstall-manual-preserved/`
- `expected/protected-path-blocked/`
- `expected/traversal-blocked/`
- `expected/broad-delete-blocked/`

## Expected Reports And Rollback Records

- `expected-reports/install-managed-section.report.json`
- `expected-reports/upgrade-v2.report.json`
- `expected-reports/drift-detected.report.json`
- `expected-reports/protected-path-blocked.report.json`
- `expected-reports/traversal-blocked.report.json`
- `expected-reports/broad-delete-blocked.report.json`
- `expected-reports/rollback-record-generated.report.json`
- `rollback-records/install-managed-section.rollback.json`
- `rollback-records/upgrade-v2.rollback.json`

## Materialization Boundary

All files are static fixture artifacts. No lifecycle apply implementation or execution, scoped transaction apply against fixture targets, active repo scoped apply mutation, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply occurred.
