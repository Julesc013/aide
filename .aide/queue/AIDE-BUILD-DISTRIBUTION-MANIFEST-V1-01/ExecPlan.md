# AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01 ExecPlan

## Objective

Build a bounded `DistributionManifest v1` protocol slice that projects existing
Q47 local release bundle evidence into a deterministic manifest identity and
validation surface. This task does not implement install, update, repair,
rollback, uninstall, publication, target mutation, or release promotion.

## Scope

- Add a Draft 2020-12 schema for `DistributionManifest`.
- Add a small Python protocol helper for manifest construction, digest
  canonicalization, validation, fixtures, and reports.
- Add AIDE Lite commands:
  - `distribution-manifest status`
  - `distribution-manifest project`
  - `distribution-manifest validate`
- Add valid and invalid fixture corpus coverage for digest, feature,
  protocol, source-kind, path, signature, SBOM, migration, and contamination
  boundaries.
- Add focused tests.
- Materialize task-local evidence and reports.

## Dependencies

- Accepted `AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01`.
- Existing Q47 local release bundle artifacts under `.aide/release/dist/`.
- Existing Q48 GitHub Release draft artifacts as publication-review evidence
  only, not distribution truth.

## Verification Intent

- Compile the new helper and AIDE Lite script.
- Run focused unit tests for schema/helper/CLI behavior.
- Run `distribution-manifest status`, `project`, and `validate`.
- Run queue inspection/evidence checks and broad AIDE validation.
- Run Git whitespace checks and commit policy check.

## Review Gate

Stop at `needs_review` with `PASS_WITH_WARNINGS` or a clear failure result and
recommend exactly `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01` if the build passes.
