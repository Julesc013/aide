# AIDE Lite Pack v0 Draft (8365aa61b7cad51d)

> Local draft only. This release has not been published, tagged, uploaded, or sent to GitHub.

## Release Metadata

- Suggested tag: `aide-lite-pack-v0-draft-8365aa61b7cad51d`
- Suggested tag created: no
- Source commit: `8365aa61b7cad51d542f88434e50bc33c5aac8fe`
- Source branch: `not-recorded-in-pack`
- Dirty state recorded: `false`
- Release type: local draft / not published

## Summary

- AIDE Lite Pack v0 local release bundle prepared for human review.
- Assets come from the Q47 local bundle under `.aide/release/dist/`.
- Install, repair, upgrade, rollback, and uninstall commands remain preservation-first planning surfaces.

## Release Notes Preview
- # AIDE Release Notes Preview
- This is a deterministic preview only. It does not publish a release.
- source_range: HEAD latest 50 commits
- source_head: 8365aa61b7cad51d542f88434e50bc33c5aac8fe
- preview_only: true
- ## Highlights
- - Security: Rollback no longer accepts a checksum-valid payload through a reparse pack boundary. (33824b369b84)
- - Added: conditional receipt-owned removal apply for exact generated material. (d13894ba0f55)

## Changelog Preview
- # AIDE Changelog Preview
- This file is generated from local Git history and is a preview only.
- source_range: HEAD latest 50 commits
- source_head: 8365aa61b7cad51d542f88434e50bc33c5aac8fe
- commit_count: 50
- malformed_count: 0
- preview_only: true
- release_publishing: false

## Install Notes

- Local install notes: `.aide/release/dist/install.md`
- Default install workflow is observe, plan, dry-run, review.
- Target repositories must run their own validation after extraction/import.

## Assets

| Order | Asset | Kind | Size | SHA-256 | Required |
| --- | --- | --- | ---: | --- | --- |
| 1 | `.aide/release/dist/aide-lite-pack-v0.zip` | zip_archive | 1040988 | `8c4fbef71470954c...` | true |
| 2 | `.aide/release/dist/aide-lite-pack-v0.tar.gz` | tar_gz_archive | 711763 | `11c95b9c10355cb6...` | true |
| 3 | `.aide/release/dist/aide-lite-pack-v0.checksums.json` | checksums | 1132 | `1cb711c1b2e4a778...` | true |
| 4 | `.aide/release/dist/SHA256SUMS.txt` | sha256sums_text | 604 | `740d6c32b0e2c4bc...` | true |
| 5 | `.aide/release/dist/manifest.yaml` | manifest | 1406 | `e4d11aa458799d35...` | true |
| 6 | `.aide/release/dist/install.md` | install_notes | 2434 | `6e6f21f90ba86ec2...` | true |
| 7 | `.aide/release/dist/CHANGELOG.preview.md` | changelog_preview_copy | 8438 | `f7b97ad091ff1b9f...` | true |
| 8 | `.aide/release/dist/RELEASE_NOTES.preview.md` | release_notes_preview_copy | 7257 | `222a04b829cac70c...` | true |
| 9 | `.aide/release/dist/release-validation.json` | validation_report | 3846 | `a457b73f186db89c...` | false |
| 10 | `.aide/release/dist/release-validation.md` | validation_report | 238 | `aa0c336c3c2c0ded...` | false |
| 11 | `.aide/release/dist/release-provenance.json` | provenance_report | 1448 | `f461068624899f3d...` | false |
| 12 | `.aide/release/dist/release-assets.json` | asset_index | 4080 | `77c865fe1939e994...` | false |

## Validation Summary

- release validate: PASS
- pack-status: PASS_SOURCE_ANCESTOR
- fixture extraction: PASS
- checksum validation: PASS

## Known Risks
- This is a local draft only; no GitHub publication, tag, or upload has occurred.
- Suggested tag naming still requires human/operator review.
- Dominium and Eureka target install readiness are not claimed by Q48.
- Install, repair, upgrade, rollback, and uninstall remain plan/dry-run models unless a future phase adds apply behavior.

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
