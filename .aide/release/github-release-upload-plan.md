# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=622224960f882e1055995c2a9ae6c408f1ba3f8ec242bfe30a5353be781040f7
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=9c16ad304636badf26f9ac1029e833e548181fa411e119574e3cd71d683a4ccd
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=ed6b9c06079c02a0bac5346fe04b842bf0f273bd3a0ff154fb74012a65843d80
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=3049c134ed66b5e33a33c2b6887cedbe00fc925929bc549442984c5ed4336e87
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=1a98a609fdec4814fa5d9b8a6ab594dcce4145f7740ce4f4530e4a51b0b61425
- 6: .aide/release/dist/install.md (install_notes) sha256=15e78170b60ffed783feb04b6d9f82f6a2867f7231e0b7809e0d584dc1b6d645
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=a7d49c6265bb2132d096817094ce44ca886e6ded573fda40367c0ea4d1c64451
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=46e5f34c74e336de105162d5b9fea0688d1ea740f55a11be805e06d3bb05b653
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=f7210173d59ebed3851081895891cd43eaea2f975baeac6f7654f8177b76ee10
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=7971268976cd00810864e3cbd6893e4c7c3bff8700a4196032ce9efc06b8c494

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
