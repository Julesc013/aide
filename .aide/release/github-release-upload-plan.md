# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=949cfc24ac261f2db520e8c1c4e80f46d9f9ac569ae6c6d5ea62c6e0c31434ec
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=26081af25c94d8494542b120ce1adee4df27710e089f65f707daecf8db679c2f
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=a0cf2ec54b47574c0db48c44cfee6d426617560cb7baf5b9cd8c847b45b89255
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=fea0853b94c327eda97b842574cd9c02f84793ae34d4bab2c87472b179fcb475
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=1db6690fdfb0d68b155354494dbcfc16fa63ed0ed8d4fec283e2324a18cec33c
- 6: .aide/release/dist/install.md (install_notes) sha256=71c1c6dca8089919a004876a4163734ce9dcf95912bd6869a542f67523ccf391
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=0d60002888bdfe5253350dffc725b6b0fda848c06e51a310f999267e42d7c1ed
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=dbc9dfe95622dcf84776bd78482c4703cd88b1c9c130b7139a4ae87b13cad758
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=2b419cdef3759992b2e6d0c9d44dc8f400c97a4713120cd3c1091eb8a308197a
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=e38d6d6c4f622e4c4ddbcad0e8567bb46fc5feab5dbb10ddbb49dd4ed6b38f14

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
