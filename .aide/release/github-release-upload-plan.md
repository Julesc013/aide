# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=0bfdfa7f6224fffe3fcbe93a4155dc2ad80db5a039cfcd57ce63f2b2cf983efc
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=aa85cc0a27c1caf9561055679f7483a82645261ec314e2b0ed211d91bd867e20
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=fd227ec0d2a78b583ccb94d98f6a850de55d58897efdb560481ce6447720e8ed
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=178a1466ff548e30940f0ffdc74c52e95a458da62131109fdb792a52e21b50c9
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=c8abe0f131a67be686b086c79a9b6ec4180c35c815d9fc4ac27c297910178622
- 6: .aide/release/dist/install.md (install_notes) sha256=0b5a5cf9b37d1968df518c788c0adc621a3f0ee3ebb28515a27e7dcaf1a66e79
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=c42acc5280fa5f2d1d00a18b2a362bf515ff3d63e411843d2d12ce45b319e37a
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=9cda7120780abcb9fe834e4938122affcb30da88abc067d27f886e9c5b5d36ac
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=410da0e7a4c0d13c3f8905729d471d855fe78fd8eab9adb22644043272714f0f

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
