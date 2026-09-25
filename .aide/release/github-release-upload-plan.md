# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=8c4fbef71470954c64dbd09e181384a3fbff0ec997a799ef197f0f6cce1e07f6
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=11c95b9c10355cb617225472cd0c72cbf8a9bbe62671d6926bd28512967aa34c
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=9436a30454a467d082e6482d965e30498d8949bc6e515707453e132ac7943a1f
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=5060e98d8094c74869b2558c31af98128d61807dc02bf977d780b4aaaed77e66
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=ed848816b777a6f6ec7c32f919ab7e9169275df634b6c2f2c6485a92ca8a7939
- 6: .aide/release/dist/install.md (install_notes) sha256=e13dd69b79d53d974cf6daee7e3b20ed1c7fed9cd57f831e9310eb4c8df4d03b
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=f7b97ad091ff1b9f40fabb51fea9409de38ba5a7f726ec3b6912bd0a2fd7169c
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=222a04b829cac70cc75860df720938453c1c9b6247e6480615b95ff4815fc42b
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=f32c20c8b0cabbe46180cc8d00b9ea9b278ab675284b6bd66b907a67aa77e892
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=5da06822463874571fcd85088d1c1cbbed2a91134fd584e61870a601d65ba244

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
