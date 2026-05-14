# Q48 Export Pack Sync

## Commands

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Pack Status

- Pack path: `.aide/export/aide-lite-pack-v0`
- Exists: true
- Checksums valid: true
- Checksum problems: 0
- Boundary violations: 0
- Provenance result: `DIRTY_SOURCE_RECORDED`

`DIRTY_SOURCE_RECORDED` is expected for Q48 because generated draft, release,
export, evidence, and context artifacts are staged for the final Q48 commit.

## Exported Q48 Support

- `.aide/policies/github-release-draft.yaml`
- `.aide/policies/release-publication-boundary.yaml`
- `.aide/policies/release-upload-plan.yaml`
- `.aide/policies/release-checklist.yaml`
- `.aide/release/github-release-*.schema.json`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q48_github_release_draft.py`
- `.aide/evals/golden-tasks/github_release_*`
- `docs/reference/github-release-draft.md`

## Exclusions

Generated Q48 draft outputs under `.aide/release/github-release-*` and
`.aide/release/latest-github-release-draft.*` are not exported as target truth.
