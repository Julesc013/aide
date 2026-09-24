# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=4b9e458fe4a3c5f67f862de9c443ea195f74df7dd0bd2d0b69a4406562fdb5d8
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=65fc3f78f719244695a80914e73d535269d486a754e61b7b0a102969705f9589
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=289db5f6b5b2a54aca47d75643f3cd44b10d9df3e6c245f66adc23c150cef8d3
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=4f8853652307830736951e881c9097148b183fec16fe481845d13f206511cafd
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=133381f86058af40f51a247ed6d737845e2cfc1d3d394c5e36d903a00dc0eb8b
- 6: .aide/release/dist/install.md (install_notes) sha256=de178573d2179a6decee863646ed9c64308eea240b26041d1c75468ceae466a1
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=62f62ff9475c5b980280d954d9228fe6356102ca8f953c9c23913ff291ef0be8
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=9c07de3ab10094fb44bfb275395d2b92e1c02e2c093cad9e242556355629174c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=57998ff0109bba9d84fbf447e8ec415d6d5dd732898d8680453e8ac85120c07c
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=8116639c5b8e34768a885e7e5fcf0f463a245b17a634bb55245760f5bf0f0cab

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
