# Release Bundle Model Report

## Summary

Q47 adds AIDE's first local release-bundle model for `aide-lite-pack-v0`.
The model is deterministic, local-only, no-publish, and uses Python standard
library archive, checksum, and extraction machinery.

## Policies

- `.aide/policies/release-bundle.yaml`: lifecycle from source validation through export-pack regeneration, archive build, checksum/provenance, fixture validation, evidence, and review.
- `.aide/policies/release-artifacts.yaml`: allowed local artifact classes.
- `.aide/policies/release-provenance.yaml`: source commit, branch, dirty state, pack hash, artifact hash, preview-only, and no-publish fields.
- `.aide/policies/release-validation.yaml`: validation gates.
- `.aide/policies/release-versioning.yaml`: `aide-lite-pack-v0` naming without invented SemVer.

## Schemas

- `.aide/release/release-bundle.schema.json`
- `.aide/release/release-asset.schema.json`
- `.aide/release/release-manifest.schema.json`
- `.aide/release/release-checksums.schema.json`
- `.aide/release/release-provenance.schema.json`
- `.aide/release/release-validation.schema.json`
- `.aide/release/release-bundle-report.schema.json`
- `.aide/release/release-install-notes.schema.json`

## Command Surface

- `release bundle`
- `release validate`
- `release status`
- `release assets`
- `release manifest`
- `release checksums`
- `release provenance`
- `release clean --dry-run`

All commands remain local-only. They do not create tags, create GitHub Releases,
upload artifacts, mutate branches, mutate target repos, or call providers,
models, or network services.

## Generated Bundle

- Bundle id: `aide-lite-pack-v0-e5a2692d3c4593aa`
- Source commit: `e5a2692d3c4593aaf9931b15adb55a201e703ce0`
- Source branch: `main`
- Publication status: `local_preview_no_publish`
- Preview only: true
- Dirty state recorded: true, because generated Q47 release/evidence outputs existed during bundle generation.

## Boundary Fixes

The first archive validation rejected an exported example path under
`.aide.local.example/secrets/`. The release archive builder now filters local
release archives against Q47 forbidden-path rules while preserving the export
pack payload on disk. Release validation confirms forbidden paths are absent
from both archives.
