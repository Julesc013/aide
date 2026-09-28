# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=a8f7c3165ef60b7995cd5799a2937255f24a3119ca545653595bc5b3cb0004f6
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=e1cc82138387c559a16ab3dc3354df603ca1951ff5bc55961844e2c04e8d5e65
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=2bf2075cf0ead75ca4259c0007a09d8283f857b6bf7c7ca3bb3fee4b82d0cc7f
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=cd5ea8b825f4698b8a4ced54dcd2a7f99ea7b3afb5ea58abf41d35bc9810ab31
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=0c5360c51a933cce83dba7e60485511a7058a04bbd924b10631a0ebae1a19d97
- 6: .aide/release/dist/install.md (install_notes) sha256=c6da737658ba6d37a941b6c8a4670d5fd3e9f5261e98455ab6c907afe0d73b37
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=04f68b4bc6b5ee4f342d798407c2807a101a68c297e839ed9f6f88d52910d4ed
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=89a368fb9b7a92b7ae00ce57b3cad04d1cb312c38cbe67d30e9837ed13e43275
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=cdb11a0f1b398ce4a6a1dc0720fcaeb2d78656e55bb44eddcb9e433288787eca
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=bb2d2d248f14ce01080a7655409ac755bf17ad0d9d56442cbb266c8a81343176

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
