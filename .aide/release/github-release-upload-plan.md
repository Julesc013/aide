# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=48b3a4a4c3f6e443cc16919b5ac7c57ddb5070f5d50bbb80cc4b559ba3bf0355
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=105f9fd774f04e8a9ef3cf0bb4dc2e5862f9f40121e92af68e1158b23d6a88d6
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=db2b38c6397e40c45ecafd15f4a42d6bea0c5673b160dfe88bd70ea70ddf7ba7
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=3de1e8791db9191381a04f7cf34b1e64e4541904afbbc64da49e930930662aa6
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=2457a72250f74efdb8fd4397dddb90e5400e3c947fc8862055fcfd3a358b729c
- 6: .aide/release/dist/install.md (install_notes) sha256=34effa204225c34d36c0e750433937dfdb5d24462fa88ac75a5f293125c8c7ec
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=c42acc5280fa5f2d1d00a18b2a362bf515ff3d63e411843d2d12ce45b319e37a
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=39b1396a9a23cd08f95cd9188676b1dc53d7da13811135af8525007fb13e87be
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=56e659ede01eb5e3b101781c717cd5ee7f5ff42a692bf4a637968737a3933d9b

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
