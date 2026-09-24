# AIDE Lite Pack v0 Draft (9dc91654f8df9d7e)

> Local draft only. This release has not been published, tagged, uploaded, or sent to GitHub.

## Release Metadata

- Suggested tag: `aide-lite-pack-v0-draft-9dc91654f8df9d7e`
- Suggested tag created: no
- Source commit: `9dc91654f8df9d7ea8b85dc32285b504f3344e26`
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
- source_head: 98de5ee1531e3d71f6f003f8bc98bf2a6b8bf23b
- preview_only: true
- ## Highlights
- - Security: refused Windows 8.3 aliases at the disposable distribution fixture boundary. (64979977922a)
- - Security: bound locally accepted GitHub checks to exact workflow-run provenance without overstating server enforcement. (cb05b135eb0d)

## Changelog Preview
- # AIDE Changelog Preview
- This file is generated from local Git history and is a preview only.
- source_range: HEAD latest 50 commits
- source_head: 98de5ee1531e3d71f6f003f8bc98bf2a6b8bf23b
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
| 1 | `.aide/release/dist/aide-lite-pack-v0.zip` | zip_archive | 980517 | `1b972fb1c96b1d67...` | true |
| 2 | `.aide/release/dist/aide-lite-pack-v0.tar.gz` | tar_gz_archive | 652765 | `9b0a5bd0943d160d...` | true |
| 3 | `.aide/release/dist/aide-lite-pack-v0.checksums.json` | checksums | 1132 | `0ee9ed3d59dc424d...` | true |
| 4 | `.aide/release/dist/SHA256SUMS.txt` | sha256sums_text | 604 | `f111e433cbb31d8d...` | true |
| 5 | `.aide/release/dist/manifest.yaml` | manifest | 1405 | `dbafe67bcdd9454a...` | true |
| 6 | `.aide/release/dist/install.md` | install_notes | 1325 | `c6964e83a0fbce03...` | true |
| 7 | `.aide/release/dist/CHANGELOG.preview.md` | changelog_preview_copy | 8915 | `e45b8dd6c1a0ceb9...` | true |
| 8 | `.aide/release/dist/RELEASE_NOTES.preview.md` | release_notes_preview_copy | 8425 | `d8ea8c8d3abbefac...` | true |
| 9 | `.aide/release/dist/release-validation.json` | validation_report | 3814 | `ac3218cb9d04de92...` | false |
| 10 | `.aide/release/dist/release-validation.md` | validation_report | 222 | `37b6d4e4c7f51060...` | false |
| 11 | `.aide/release/dist/release-provenance.json` | provenance_report | 1448 | `5cbeb388a943e616...` | false |
| 12 | `.aide/release/dist/release-assets.json` | asset_index | 4079 | `541ea57bcbe98fa5...` | false |

## Validation Summary

- release validate: PASS
- pack-status: PASS
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
