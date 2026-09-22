# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=b5cc171d178a404df125ddef0c8cb8d8bef50ecfd72329c7995bad127b5b437c
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=b50b116737ab65036e8fa520c4b729b5b58dd1caa1069774bcf8b8022706ef36
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=6e5515eadc0f10ad78441b37c6e44ce4ab60372dd55bfa0cd9ae43de87eb4a74
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=015f320dbd2942ebf2a13e8ecc93aa126cdfbf5ca8bf6ebe016883cb212a6061
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=b27b8b16a2bf8dddf8ca6b89f1f4f2507435167896f05ae6c302bd4bb4c7bb6d
- 6: .aide/release/dist/install.md (install_notes) sha256=cb2637ef75783b6e2c0e6a3638a60dea7b594d5327256dbb8ac4d393cf8b0744
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=11e1700d29651d67f662840ff510d89c2cd53d0fd97754c0a621f36a81cc37b3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=1503f3018b64c0f56caa5c8e4566776e88b5f8d78a84e4f076e742697e461b33
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=1f361eda6c1688e709a4931468835f17e49ebefa1fc3e927a06169c30e9114f6

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
