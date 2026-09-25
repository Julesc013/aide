# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=32c1f0ad5465809eec5d8ed64c801e8d3ca31c0fe5840ca41188a376325711f9
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=22101aa98982cf8b88d6a4540d814e9751095207535427a4e5a5fc3f36833044
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=c658f8a3fb4d2446037889ca042eed74adacfe7951f0be50a3070f1a09e89e62
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=310c20418897721fb395292de85c0dfd6799c1c07c9b783538b6833865438a3c
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=4792720faa2f7dca979a1b28cf0fc07a29e4a8f91490e36f224790580d24558c
- 6: .aide/release/dist/install.md (install_notes) sha256=38114b389335e6e14711130b171c89a64fe9085562434515f5c8f4c0a2c3ec68
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=d809961de7600adb6a262616a657564c273b6ebd2a9502de19e87be5989d5dc3
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=d4119bd0ff7760c53f1cc3376608c3bfebbc4d3df06d37ea417f695f0065639b
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=214c150a1be52f9fa1171b382a68a8895faefe4a2f4e7b8d0e3fcf49d0a3f7aa
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=aad7d9bc38d4a5ad405301ccb8817db97858ad63855f1bd4a1b441410319cbbb

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
