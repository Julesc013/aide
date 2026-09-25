# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=68f8b3cc07c6476999828577c59bdb8785d13509613d0351a617908c99fa784c
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=d0b424563ea7a85d207546b0e2b0d381641e046659846876adbddf96a954073b
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=4c5f89fdcda6e018f0e3e8734988f32cd640a6425c030a3a5284414fa224a9a9
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=47ad6069217daa21eb4e73f1d34cded293d7c945d9dc8fdb344609cecc7b4acb
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=f487170430af34d065c48a0dfdcac52076d5a11ca1d0f15afb5fd402a1b92462
- 6: .aide/release/dist/install.md (install_notes) sha256=8d0ef079298c5546340511becf6672bad3a463496afee4bb6647eb8335c42f7b
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=e7a98808fc8b7ede1656fc5cdf770e8876886ca08086dd73901dd57e51d0e20f
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=9c7d559903ae79b75abef3efd9cdfb136e0dbea7d9520e705b3837d3449c0662
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=7afee19d97a1dd22c0d68bc9a9064cfee1b01001558cfd9d7a86cebf05310599
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=ba5cbce5d9da9a9268621697b0a537844d09d3ebfef8bda3f04b9a2f19d6aba4

## Blocked Actions
- create_git_tag
- push_git_tag
- create_github_release
- upload_release_asset
- publish_package
- mutate_branch
- mutate_github_settings
- install_ci
- call_network
- call_provider_model

## Prerequisites
- release bundle validation pass
- pack-status pass
- draft validation pass
- secret scan pass
- asset list reviewed
- publication checklist reviewed
- explicit operator approval
- tag naming decision
