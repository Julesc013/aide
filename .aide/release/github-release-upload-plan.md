# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=d1eaf1bcb7272492b0a4dacf8cd2e291a54471a1051cae002d24c08bb8fb5f00
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=ce3066076029d7f0e63172840f838ae4cfd141ae041760663800e72f4b0b218e
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=5f3ee01e5775cbe6f95607c5569430a5233639041e493b61c240c57999cf9816
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=ebca00da041abf3f5add7fe0d0d2a1f6a1d7835dd7e03d90275ca2cc2d7e933c
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=da06b3679d5dba08dc2cf522cfe2fc19e654b6ed716be2b16453cfd61b655bb0
- 6: .aide/release/dist/install.md (install_notes) sha256=4ce8b603deff3f817f4b1ad0c58294c6e80b6626c3bd64e343671df6f7bdb977
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=b86d4e79378a8fefa8f5be2d25f94cede66f98968b5f262a278c76b9beaa59bd
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=97ad9ea58d613945c88173f5a5d8f316d56b0cf9f2babb9c41e02a1545fd5182
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=70ad198b819481b8c1a3f71d012fe11204e3f7ea62ea3ddbd7691d56f5130735
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=cc77d0abf99b69ddfc98f9d216f3d6a0928b1c1bec1c921962783073c3afe1c8

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
