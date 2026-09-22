# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=ad2e50daf391ce760d24d45fbbdcf178b12f8685a925cb8a240100e4ddb20028
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=01cabce16417175855f75f87fe4d6b1b25373007644be536b2b9bb114ea6b328
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=010f72abc3ebf1f147065f755ecdc080614bece2e2c84ae45636a464ec7769e0
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=2d076e0124a5589b6275cfc1bf383ac003142fb919828928dc92a1d9df701b8c
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=84d36396300b7c032d5727904f8aa4255c433f51bd87328378359d45c43573a0
- 6: .aide/release/dist/install.md (install_notes) sha256=54b3aaf3aba0744291ff84ce7bd1c0a9154fdc9f77816910eee5f00b2f8bbc9b
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=fa94ab8f8c1a08931063994878e7566c56a23bba7d8bdac57e4c1aa4108c531b
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=418faf9e0437f2e86155c7448194e2314457d9a7ec7f6bcc132d2ec6cc8c8a9b
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=406d9951c59112721e10cb9b9a6f7277227d20976ca900ced7ad68c53e250a49

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
