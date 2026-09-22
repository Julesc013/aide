# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=32156c0ab2ee8a1d77c7613af6a25846256ca3de60db93e8900a42ffb2008c7f
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=1071c9001b75b8df43ce6122d5145afc55b5004cd70d9b4ffdcd7b58d4f3fa69
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=3663543c6273a87fc6f5d9e63ccb0c64073e16e08e83dcc9ac78677c26320eeb
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=59034e9213c1e02d42f87abaa11b615d4347ae02cdb50b34879c00d5b5a5cbd4
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=0e8396b4b1e06cbf2234fd09a3bc5cff43d44f91b38a40c0cb064ae63053a316
- 6: .aide/release/dist/install.md (install_notes) sha256=29c58a483b02f9094748da088614b9064f4d5f5308543da970a8adc8aa80c9df
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=d01fbfd9f5e4766338df3049b3089d9d923566ba87adc7bb45e27016799c41e0
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=bfec95af6e4d97cfdff91885139016a75d030b4aff9f170dc7bca832415ad251
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=87b67bb7ec7a8b41ef6d2e74d9a37f4b94dd9876b97839682b322ee05c731cf0

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
