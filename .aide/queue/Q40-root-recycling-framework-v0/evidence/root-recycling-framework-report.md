# Root Recycling Framework Report

## Policy And Command Surface

Q40 adds a deterministic, repo-local, no-call root recycling framework. The
active policies are:

- `.aide/policies/root-recycling.yaml`
- `.aide/policies/root-inventory.yaml`
- `.aide/policies/root-fates.yaml`
- `.aide/policies/root-exceptions.yaml`
- `.aide/policies/root-risk.yaml`

The AIDE Lite command surface is:

- `roots inventory`
- `roots classify`
- `roots plan`
- `roots validate`
- `roots status`
- `roots explain-root ROOT`
- `roots explain-file PATH`

## Generated Artifacts

- `.aide/roots/latest-root-inventory.json`
- `.aide/roots/latest-root-inventory.md`
- `.aide/roots/latest-root-classification.json`
- `.aide/roots/latest-root-classification.md`
- `.aide/roots/latest-root-recycling-plan.json`
- `.aide/roots/latest-root-recycling-plan.md`
- `.aide/roots/root-exceptions.json`
- `.aide/roots/root-risk-summary.md`

## No-Apply Guarantee

Q40 generated artifacts record:

- `no_apply: true`
- `file_moves: false`
- `file_deletes: false`
- `reference_rewrites: false`
- per-file `apply_allowed: false`
- `drop_candidate_is_deletion_approval: false`

`roots validate` fails if root classifications or plans contain apply-enabled
records, deletion approval language, or tracked local/secret state.

## Boundary Fix

Final validation found that Q39 refactor selftests were accidentally made to
require Q40 root outputs inside a fixture. Q40 corrected this by keeping Q39
generated-output validation scoped to Q39 refactor artifacts while Q40 owns root
artifacts through `roots validate`.
