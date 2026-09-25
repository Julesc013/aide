# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=956b59a76d7d8d42cbeb83d776beab7cf096c4ff964314f4252e1e0531f4b4fd
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=4dd239edd4d52ab25bb4b41cb0eb9b756710894e5f4d0400defd9305d255606c
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=168c7364d78f7bf2b42c1ab8f1afe5636a8dfcfa00fb4e77ca296036ff3c6adc
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=1b0d070d8251b4e8bf175750fca14a9fbf34786711cd25ed4e9de83080929156
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=7bca7ebc8e943147e92823f3ef659ec8ce44e1309d570e3442aff0f3cd83d1b2
- 6: .aide/release/dist/install.md (install_notes) sha256=1ac57d7c8ba8f07355c67c5a24b89a44c44274c563aaeb157d3c015cece2d350
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=24a6f5a2c48fc2d64c9096cbbfb271e12b5c6e0876c32c19ca4f3c9f22747797
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=05ccee6aa7db25166c63d201b09c2676d3b583e4f596f094ee03761433c7211c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=de378b0a64a4c1d7e958d272eff439be6b5d0f4ecb9ec894ca942a88a3e3b73d
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=89cb21195c3bdfc0d6e2e9ceb3a89e8c8675b5e86a2a2122eb82d76fa70eb8c9

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
