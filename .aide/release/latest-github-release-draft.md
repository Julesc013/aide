# AIDE Lite Pack v0 Draft (65fafcc9f5bed0a3)

> Local draft only. This release has not been published, tagged, uploaded, or sent to GitHub.

## Release Metadata

- Suggested tag: `aide-lite-pack-v0-draft-65fafcc9f5bed0a3`
- Suggested tag created: no
- Source commit: `65fafcc9f5bed0a32a5f9aaaa0155a815e0f3599`
- Source branch: `not-recorded-in-pack`
- Dirty state recorded: `false`
- Release type: local draft / not published

## Summary

- AIDE Lite Pack v0 local release bundle prepared for human review.
- Assets come from the Q47 local bundle under `.aide/release/dist/`.
- Q43-Q46 report-only planners and separate bounded Windows exact-plan apply commands have distinct boundaries.

## Release Notes Preview
- # AIDE Release Notes Preview
- This is a deterministic preview only. It does not publish a release.
- source_range: 8912eab9071cd2599fb4f43721aa0dafea807a8e latest 50 commits
- source_head: 8912eab9071cd2599fb4f43721aa0dafea807a8e
- preview_only: true
- ## Highlights
- - Added: Explicit one-turn Codex job adapter in the existing Lite runner. (651744c0a428)
- - Added: Include the portable bounded job interface in the Lite release contract. (20710eace078)

## Changelog Preview
- # AIDE Changelog Preview
- This file is generated from local Git history and is a preview only.
- source_range: 8912eab9071cd2599fb4f43721aa0dafea807a8e latest 50 commits
- source_head: 8912eab9071cd2599fb4f43721aa0dafea807a8e
- commit_count: 50
- malformed_count: 0
- preview_only: true
- release_publishing: false

## Install Notes

- Local install notes: `.aide/release/dist/install.md`
- Preview first; use documented exact-plan apply only where the final artifact and Windows profile are qualified.
- Target repositories must run their own validation after extraction/import.

## Assets

| Order | Asset | Kind | Size | SHA-256 | Required |
| --- | --- | --- | ---: | --- | --- |
| 1 | `.aide/release/dist/aide-lite-pack-v0.zip` | zip_archive | 1111952 | `070c5d2c8bd36b44...` | true |
| 2 | `.aide/release/dist/aide-lite-pack-v0.tar.gz` | tar_gz_archive | 777969 | `b17ca0b0c44da360...` | true |
| 3 | `.aide/release/dist/aide-lite-pack-v0.checksums.json` | checksums | 1132 | `9a0be7027b706a52...` | true |
| 4 | `.aide/release/dist/SHA256SUMS.txt` | sha256sums_text | 604 | `8a69ba6eea083d21...` | true |
| 5 | `.aide/release/dist/manifest.yaml` | manifest | 1406 | `0b680d3e98683e12...` | true |
| 6 | `.aide/release/dist/install.md` | install_notes | 2434 | `3899ad4e34397f26...` | true |
| 7 | `.aide/release/dist/CHANGELOG.preview.md` | changelog_preview_copy | 7024 | `8edb41c9724a05a6...` | true |
| 8 | `.aide/release/dist/RELEASE_NOTES.preview.md` | release_notes_preview_copy | 5807 | `3a29b38ca16e8615...` | true |
| 9 | `.aide/release/dist/release-validation.json` | validation_report | 3846 | `a457b73f186db89c...` | false |
| 10 | `.aide/release/dist/release-validation.md` | validation_report | 238 | `aa0c336c3c2c0ded...` | false |
| 11 | `.aide/release/dist/release-provenance.json` | provenance_report | 1448 | `e0a471ce4f4879ce...` | false |
| 12 | `.aide/release/dist/release-assets.json` | asset_index | 4080 | `2beae63f3df285df...` | false |

## Validation Summary

- release validate: PASS
- pack-status: PASS_SOURCE_ANCESTOR
- fixture extraction: PASS
- checksum validation: PASS

## Known Risks
- This is a local draft only; no GitHub publication, tag, or upload has occurred.
- Suggested tag naming still requires human/operator review.
- Dominium and Eureka target install readiness are not claimed by Q48.
- Q43-Q46 lifecycle planners remain report-only; separate Windows exact-plan apply paths require final profile qualification before public support is claimed.

## Publication Blockers
- none for local draft generation

## Manual Publication Checklist

- Review this release body.
- Review suggested tag naming.
- Review asset list and checksums.
- Review known risks and target install caveats.
- Decide whether the eventual GitHub release is draft, pre-release, or stable.
- Obtain explicit operator approval before any future publication phase.

## Non-Publication Statement

- tag_created: no
- github_release_created: no
- upload_performed: no
- network_api_call: no
- branch_mutation: no
- active_ci_installed: no
