# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=e7e14b8e112ddcd762022c26b59deaa3aff1b49f69950fc2f4751e7fedf3e8c8
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=06852530d459271184022d17a11f514a8402351354683cae49899678100f0699
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=b02340548a79e203983e8adce4c93f7941fe82a2d2632782968e7dabd611fbdf
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=8ce20661d2c75ce8535e674ba94fa80ca122338caaa3ebd21f1c190d368ea7da
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=af05ade78525e720b6b4e45e837dc95caa91772d7aaea12fa79052a91d220e74
- 6: .aide/release/dist/install.md (install_notes) sha256=8bf5e95ded5572a4bf2b7b5f61bc171d51b0a7103d27a8e6285b8ce41df93b19
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=662f9a61099bd9e573d2aa85726264c44b0471e0a5b95eaf4853068a9ad80dec
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=7d8dd1c2ba9154d1ddfbbd94e2544097f20dc5ca9ea50455ba90fa89073f80a9
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=7bcfa3600a204a90335734ffdce86bf8e10b42c28f5f8eaf68b9603566482a40
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=99093fa72b751845d8040f0de1cf9de9bea3947a8133a3de8624599aab75f5c8

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
