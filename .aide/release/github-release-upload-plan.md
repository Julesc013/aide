# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=8fb17229ac54d9355170a28b6e4bce3182cf6ad1078d4e30c81f7d5ea461d660
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=a92d468eaedba29abb79557851ed3fe5226c6bcfda2a522ed9fb13d2548e93d7
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=b24f658d967742a89a5e136757af351003ad942a9952c6c4276c65cb5b6dc57b
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=b5f84d4dc523d9cc238cae37bcfaf3e88914210455200d541d3dbcd727d19721
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=0cc9793f69c9099f11bceb8f3d144d5cddc0d61bb25d99036420ecb0a4803065
- 6: .aide/release/dist/install.md (install_notes) sha256=0c3798a4e10ed6f083f4d1b9fcd7c75ea0e54a66bef3e995a2ea0e564fbe244d
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=5469c48909af069e164918de9cddd0bc0f702411e59bfb6ad8eeab3526823e3e
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=52dd1ed2bb305a45a59ec5ca2cb55eba8c8316b17d1c8b89c127789d8fd89b02
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=746317110fd2e5cc0a6fcd41715839045d11232ce0b5e011a6658d56166528af
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=df35747cfd0d9361cf1dfd5d36a185bceb5e4939f0f892bb7dbb97da16040aae
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=70afe5f78256cde212642a9117be1d98ee9d5d998d6fc4b478387312d7a956b0
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=38b365a989a89a9d713d142409d70472e27967d7c446d1c0fddd2a9c2c7978aa

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
