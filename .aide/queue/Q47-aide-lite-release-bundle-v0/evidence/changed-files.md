# Changed Files

## Queue And Evidence

- `.aide/queue/Q47-aide-lite-release-bundle-v0/**`: Q47 task packet, ExecPlan, status, prompt copy, and evidence.
- `.aide/queue/index.yaml`: Q47 added and moved to `needs_review`.

## Release Policies And Schemas

- `.aide/policies/release-bundle.yaml`
- `.aide/policies/release-artifacts.yaml`
- `.aide/policies/release-provenance.yaml`
- `.aide/policies/release-validation.yaml`
- `.aide/policies/release-versioning.yaml`
- `.aide/release/README.md`
- `.aide/release/release-*.schema.json`

## AIDE Lite, Tests, And Golden Tasks

- `.aide/scripts/aide_lite.py`: added the local-only `release` command family.
- `.aide/scripts/tests/test_q47_release_bundle.py`: release policy, schema, archive, checksum, fixture extraction, forbidden-path, and dry-run clean coverage.
- `.aide/evals/golden-tasks/release_*_golden/**`: Q47 deterministic release goldens.
- `.aide/evals/golden-tasks/catalog.yaml`: release golden task entries.
- `.aide/evals/golden-tasks/upgrade_*_golden/**`: missing Q45 catalog entries materialized so full eval runs stay coherent.

## Documentation

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `AGENTS.md`
- `docs/reference/aide-lite-release-bundle.md`
- `docs/reference/cross-repo-pack-export-import.md`
- `docs/reference/aide-install-model.md`
- `docs/reference/aide-upgrade-model.md`
- `docs/reference/aide-rollback-uninstall.md`

## Generated Release Artifacts

- `.aide/release/dist/aide-lite-pack-v0.zip`
- `.aide/release/dist/aide-lite-pack-v0.tar.gz`
- `.aide/release/dist/aide-lite-pack-v0.checksums.json`
- `.aide/release/dist/SHA256SUMS.txt`
- `.aide/release/dist/manifest.yaml`
- `.aide/release/dist/install.md`
- `.aide/release/dist/CHANGELOG.preview.md`
- `.aide/release/dist/RELEASE_NOTES.preview.md`
- `.aide/release/dist/release-validation.json`
- `.aide/release/dist/release-validation.md`
- `.aide/release/dist/release-provenance.json`
- `.aide/release/dist/release-assets.json`
- `.aide/release/latest-release-bundle.json`
- `.aide/release/latest-release-bundle.md`
- `.aide/release/latest-release-artifacts.json`
- `.aide/release/latest-release-validation.md`
- `.aide/release/latest-release-provenance.md`

## Export Pack

- `.aide/export/aide-lite-pack-v0/**`: regenerated to include portable release policies, schemas, commands, tests, golden tasks, and reference docs.
- Source-generated release outputs under `.aide/release/dist/**` and `.aide/release/latest-release-*` are not exported as target truth.

## Generated Context

- `.aide/context/latest-task-packet.md`: regenerated for `Q48 GitHub Release Draft v0`.
