# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=515817522aba08281cb7f61a55185fbdc315b861d002d2008b3a3d94d7235411
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=c5def15fc3920d25aad095ede0ea4f39966f8cff2e082c4ba06facb5414d5bbb
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=1a44378e86fd7a63273ae890c3ac0b9fb6db4f46870c74584370c1a9a9499e07
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=8ee246cf486f586c7667b43795f820628985018c4ac3785624ebac957aa5e7df
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=25565aef8a91ebe110a81112947a90d5c4564b156e863011e4d6cacbe2d40c1c
- 6: .aide/release/dist/install.md (install_notes) sha256=b4bdcff9b34999b25fd458ce12a10496c4fe53e8a2f5d89c75771e71732cbfd3
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=5ba015ec96f7b72c590516856e6297f0c1daeb03f10c655162e85bb72b1312b1
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=5e27dccc8ca665359949e39a61d7133ebf7b1aad44b8ffb17eaf42b135f869ae
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=9eb37ddb251b5ad8fcf3e669689abbfc9010c03275d37b5f6add0ed60676dc5b
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=7883b0d6eb509381b7ec3b9bc60dc24adba92898b9fff8cddb310fcc73480c93

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
