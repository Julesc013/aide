# AIDE Lite Pack v0 Draft (d0c8f62ce94465a6)

> Local draft only. This release has not been published, tagged, uploaded, or sent to GitHub.

## Release Metadata

- Suggested tag: `aide-lite-pack-v0-draft-d0c8f62ce94465a6`
- Suggested tag created: no
- Source commit: `d0c8f62ce94465a6c174de4e931db10d1ba451ea`
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
- source_head: aab0756968fd8aededc247f5e01f028818068594
- preview_only: true
- ## Highlights
- - Added: Separate first-stable Lite candidate archive generation and validation. (24bd7d0d88c6)
- - Added: Distinct local AIDE Lite 1.0.0 candidate assets for final qualification. (92da95735736)

## Changelog Preview
- # AIDE Changelog Preview
- This file is generated from local Git history and is a preview only.
- source_range: HEAD latest 50 commits
- source_head: aab0756968fd8aededc247f5e01f028818068594
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
| 1 | `.aide/release/dist/aide-lite-pack-v0.zip` | zip_archive | 1064803 | `8413a071db72ebcf...` | true |
| 2 | `.aide/release/dist/aide-lite-pack-v0.tar.gz` | tar_gz_archive | 735517 | `739868e0f1c46cff...` | true |
| 3 | `.aide/release/dist/aide-lite-pack-v0.checksums.json` | checksums | 1132 | `6b04ad3bed64075a...` | true |
| 4 | `.aide/release/dist/SHA256SUMS.txt` | sha256sums_text | 604 | `a421300e818835b3...` | true |
| 5 | `.aide/release/dist/manifest.yaml` | manifest | 1406 | `697c0ed20929ce06...` | true |
| 6 | `.aide/release/dist/install.md` | install_notes | 2434 | `4b1cbfc21cd0a14e...` | true |
| 7 | `.aide/release/dist/CHANGELOG.preview.md` | changelog_preview_copy | 7847 | `263cd047e995a967...` | true |
| 8 | `.aide/release/dist/RELEASE_NOTES.preview.md` | release_notes_preview_copy | 6246 | `e65344ad19f7d738...` | true |
| 9 | `.aide/release/dist/release-validation.json` | validation_report | 3846 | `a457b73f186db89c...` | false |
| 10 | `.aide/release/dist/release-validation.md` | validation_report | 238 | `aa0c336c3c2c0ded...` | false |
| 11 | `.aide/release/dist/release-provenance.json` | provenance_report | 1448 | `07e944a15ce9fda2...` | false |
| 12 | `.aide/release/dist/release-assets.json` | asset_index | 4080 | `7572536fe58ecbf3...` | false |

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
