# Q48 Changed Files

## Queue And Evidence

- `.aide/queue/Q48-github-release-draft-v0/**`: Q48 queue packet, status, ExecPlan, prompt, and evidence.
- `.aide/queue/index.yaml`: marks Q48 as `needs_review`.

## Policies And Schemas

- `.aide/policies/github-release-draft.yaml`
- `.aide/policies/release-publication-boundary.yaml`
- `.aide/policies/release-upload-plan.yaml`
- `.aide/policies/release-checklist.yaml`
- `.aide/release/github-release-draft.schema.json`
- `.aide/release/github-release-asset.schema.json`
- `.aide/release/github-release-upload-plan.schema.json`
- `.aide/release/github-release-checklist.schema.json`
- `.aide/release/github-release-publication-boundary.schema.json`
- `.aide/release/github-release-draft-validation.schema.json`

## AIDE Lite, Tests, And Golden Tasks

- `.aide/scripts/aide_lite.py`: adds release draft, validation, status, upload-plan, checklist, and publication-boundary commands; also hardens install observation scans to skip binary release archives.
- `.aide/scripts/tests/test_q48_github_release_draft.py`: covers Q48 policy/schema validation, draft generation, missing assets, checksum mismatch, no-upload plans, and publication-boundary gates.
- `.aide/evals/golden-tasks/github_release_*`: Q48 no-call golden tasks.
- `.aide/evals/golden-tasks/catalog.yaml`: registers Q48 golden tasks.

## Documentation

- `docs/reference/github-release-draft.md`
- `docs/reference/aide-lite-release-bundle.md`
- `docs/reference/cross-repo-pack-export-import.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `AGENTS.md`

## Generated Local Draft And Release Artifacts

- `.aide/release/github-release-draft.md`
- `.aide/release/github-release-draft.json`
- `.aide/release/github-release-assets.json`
- `.aide/release/github-release-upload-plan.md`
- `.aide/release/github-release-upload-plan.json`
- `.aide/release/github-release-checklist.md`
- `.aide/release/github-release-checklist.json`
- `.aide/release/github-release-publication-boundary.md`
- `.aide/release/github-release-draft-validation.json`
- `.aide/release/github-release-draft-validation.md`
- `.aide/release/latest-github-release-draft.md`
- `.aide/release/latest-github-release-draft.json`
- `.aide/release/dist/**`: regenerated Q47 local bundle artifacts used as Q48 draft assets.
- `.aide/context/latest-task-packet.md`: regenerated for `Q49 Dominium Fresh Install Preflight`.
- `.aide/context/latest-review-packet.md`: regenerated Q48 review packet; review-pack warns only on the inherited token budget threshold.

## Export Pack

- `.aide/export/aide-lite-pack-v0/**`: regenerated export pack with Q48 release-draft portable support. Generated Q48 release draft outputs are not exported as target truth.
