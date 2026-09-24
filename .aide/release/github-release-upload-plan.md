# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=787759eda0c0d4c159106b0eec271eb876a099133d462180a50c06a2077d89c8
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=437fdefcf524ff2a7d7918d34554bb84f18df810a4aaa27465019260182da435
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=fb068763246a4d39d3a4d04f41b299ef20388c6806752b6e3fcbd9ad6e337aa8
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=2a93d104ccd80774d6563b50fedc952fcf39eb9f172fa486a9b1f851e1b26d80
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=0f132ab6c2e8f643602cd35bcc3fd01cd24a0cb8b89ec6502578eb4d65d8a5ba
- 6: .aide/release/dist/install.md (install_notes) sha256=ea7c2c0da6539d315a68fb55afa71c1ec623a40230b3bc2deaa2d0461f8eaea9
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=27424d692791c852fc290c07dca165545e4f74f0b0cc95ca931ce0fe75505731
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=95a114721e2f4d7551d0e374378cbec86f5f57b68cf2201e3357d3900050a770
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=e422d2387ac638ea841bbc613450e58bfe5925eb7978fc682f58a936d33f3b34
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=443e373ca82b05c4e3a809fa658877b2b60f2b07525d5633970235c5f41e5ea8

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
