# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=1c797d61f5c559b1e3424c71dc7306095e3438e2184351a3e02ff464c4b43fd8
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=b2d4dc7d5ef52c0bad0394bb6cf80d14dc1fa09ea7f93147c51d03f6473588f6
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=c550eec2b700f6ddb1db858420f56cf3303637d2abc042d6dbe2bf257eb3ed0e
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=ea072f116ac1bb982abff446cf24abbb89dc20efa7baeb76e5bb3b0880d68712
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=03a935e9c2390ec0d05d4dfc4c238a7cc2ef19b8602ac2eb4c120c6a541074e3
- 6: .aide/release/dist/install.md (install_notes) sha256=0d490b36dd0708ad040c2f2bf5a3fd861a8e2b0d6a7f789a2330ba3454831e23
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=dcbce43079b9d56688c9a718468b3f63fc123be6d0f6a11f30555103d94cffd4
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=e5e2ba4893055be8bc19ce1c03ce25713efdbacbe005d90c14dd107af785caca
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=b6a61e46fc3c0f1261ac3f83ef8a8b283eb751bd4681a6ebb1ef240bb31310e1
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=1badc2438785d8d5ac4db37e09a6e08855d6264bec0d72118a00ba6186a3b5e3

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
