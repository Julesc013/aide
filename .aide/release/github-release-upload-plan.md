# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=b5cc171d178a404df125ddef0c8cb8d8bef50ecfd72329c7995bad127b5b437c
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=b50b116737ab65036e8fa520c4b729b5b58dd1caa1069774bcf8b8022706ef36
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=de06771fb26d1c38d1bd095f41eceafa090b0d37689a7be70a8688d64c25fbda
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=35dcbf96df81481a0a35d12dc9399d9fa85f67c5125d515da7125176fa13148d
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=10f67210f5e8c95cdca2e906d02e5bc83ee9bf94f99bfa1fec907a49a5e1772c
- 6: .aide/release/dist/install.md (install_notes) sha256=781d161d024e6f9ab202e77e46d900f0f247c989a121402a96ac22664e57fd80
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=fa94ab8f8c1a08931063994878e7566c56a23bba7d8bdac57e4c1aa4108c531b
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=b61128dc9553499e81b7adf65e3ec6ac057399b95f0aa42acc7cb77065f63dad
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=80c5927dc6fa81a877f10e0b4e60b0364a9b0db76a5319621d5452e41e8610d5

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
