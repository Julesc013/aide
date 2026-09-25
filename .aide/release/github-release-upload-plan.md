# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=d1eaf1bcb7272492b0a4dacf8cd2e291a54471a1051cae002d24c08bb8fb5f00
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=ce3066076029d7f0e63172840f838ae4cfd141ae041760663800e72f4b0b218e
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=0cc9f37bad932cc4ccc782a42c224754ffaea13fc0ffcb91ea1f0184ca2546e3
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=e5cee7b9d066d5de0e35a7ce900c2f28dc5eb3f22fa1d44f252e12ea130278ac
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=f1d9297f1f86512f10362af2f2a0d11c77749cd878dd6be8ff34525ec1c2080c
- 6: .aide/release/dist/install.md (install_notes) sha256=95a75c1019c749ae3f5e0a213afa4bb01bbe903688e3b78824a79ab258d49c0e
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=a3e381d574a01ad30e1b30820d2ef78e83bdc16412ceddfc2ad424ea8fb9cc7d
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=f38f9e4132d301b42429b1b56f4dedfe657057857fe117eb6df49d1cc7e2149f
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=51f510928398624698277f053554ae8de36931e8e3922871c3ad4fd5056724c2
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=64af89003a2dad276c13fdeff19c8fe1555a9e485a4a65d2b483a823a2ce0439

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
