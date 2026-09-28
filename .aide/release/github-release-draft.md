# AIDE Lite Pack v0 Draft (4b5854f2f9dbeea7)

> Local draft only. This release has not been published, tagged, uploaded, or sent to GitHub.

## Release Metadata

- Suggested tag: `aide-lite-pack-v0-draft-4b5854f2f9dbeea7`
- Suggested tag created: no
- Source commit: `4b5854f2f9dbeea7cf246946caf02d829a16c757`
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
- source_range: HEAD latest 50 commits
- source_head: 4b5854f2f9dbeea7cf246946caf02d829a16c757
- preview_only: true
- ## Highlights
- - Added: explicit bounded maintainer job inspect/run/recover commands. (5ea1f7cdd53c)
- - Changed: Task OS golden validation leaves source projections unchanged. (e185d2898fb2)

## Changelog Preview
- # AIDE Changelog Preview
- This file is generated from local Git history and is a preview only.
- source_range: HEAD latest 50 commits
- source_head: 4b5854f2f9dbeea7cf246946caf02d829a16c757
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
| 1 | `.aide/release/dist/aide-lite-pack-v0.zip` | zip_archive | 1056567 | `af8bf103353d72ea...` | true |
| 2 | `.aide/release/dist/aide-lite-pack-v0.tar.gz` | tar_gz_archive | 726805 | `f0111bd834eb1aeb...` | true |
| 3 | `.aide/release/dist/aide-lite-pack-v0.checksums.json` | checksums | 1132 | `e269877184c63248...` | true |
| 4 | `.aide/release/dist/SHA256SUMS.txt` | sha256sums_text | 604 | `69a6f01fe006d89b...` | true |
| 5 | `.aide/release/dist/manifest.yaml` | manifest | 1406 | `b48bcd3a7a33779a...` | true |
| 6 | `.aide/release/dist/install.md` | install_notes | 2418 | `a8671664ea0d2731...` | true |
| 7 | `.aide/release/dist/CHANGELOG.preview.md` | changelog_preview_copy | 8214 | `81bc162e3f9995bf...` | true |
| 8 | `.aide/release/dist/RELEASE_NOTES.preview.md` | release_notes_preview_copy | 6595 | `f9c9d1c3a9f67dba...` | true |
| 9 | `.aide/release/dist/release-validation.json` | validation_report | 3814 | `ac3218cb9d04de92...` | false |
| 10 | `.aide/release/dist/release-validation.md` | validation_report | 222 | `37b6d4e4c7f51060...` | false |
| 11 | `.aide/release/dist/release-provenance.json` | provenance_report | 1448 | `0352f5786685c4bc...` | false |
| 12 | `.aide/release/dist/release-assets.json` | asset_index | 4080 | `e89fe8cb0dbf7b24...` | false |

## Validation Summary

- release validate: PASS
- pack-status: PASS
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
