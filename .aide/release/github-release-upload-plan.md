# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=be9d0d77151c1206fd2119401f81ffb58bb62a38f8fb6a7dda4490cb7718c555
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=b444e546f3b7564e920389e5a9618fbf44a85a52f5676e5b6b7a82d33bab24ac
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=08421daa743030fbadb34689ee6124b422b1b3171564b34e1f61540716fe2a3b
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=87d5192195dfca00e997ba135ed8717ad196d3c5c593afbdef5d4bcba137c1b7
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=0fef68da6c0e16c274508485f4d945ba37ed3866ed2059a31f427ed6082095c8
- 6: .aide/release/dist/install.md (install_notes) sha256=6ea552128cc01823df51df1519a776b9e1aa00c14d178e7645154cb360afc579
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=416870cfce568c36034590eb19b372994c35ad34fb69b3b75a2c1931b8fd387a
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=164073e1fa6e63ce8a52acc9b5dca73b3106c3bb9bf4e6a9ec6db7b8f60de198
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=a33256e18a901f499623b4555c732be313f2a2f5bedc807ca95f13f9087f1bb7
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=3584696e36c6ed457a97ef1ded0a353014db73db46df7ed32c37ed1cc368650c

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
