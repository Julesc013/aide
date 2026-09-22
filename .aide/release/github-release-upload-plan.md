# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=3f24c8e27e21c1884c866ad4faf15538a1fd53cb2905e9d9abe41f6fbe170905
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=fb855c0e88d26138014038ff3ed5c2c5f2fc26a57f08fafd0f842492a327e758
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=79c07dc12fadb726ad2841626e5a2ab29c90c1a68f9d47c5c2766dfd2695e6ab
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=fee18729126d3829de10d5e55cd117123ef662136c9d6efd83b8287f6b6efc6d
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=1411165c7d4d0f0382d4d8c828c856ebce38f4ac81305da6c55a56f7c3d1ccb4
- 6: .aide/release/dist/install.md (install_notes) sha256=e998dfd86096d6f2d1b3e33a107ddaf1b618210860c773b754621ce5f69333eb
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=fa94ab8f8c1a08931063994878e7566c56a23bba7d8bdac57e4c1aa4108c531b
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=7d5b0df3e71b2b741b7b5a2e6101c42e22b3e91a231546148c769b45bdd050e1
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=57d278050e24186db6d9a2d68f4e80b32b62948c63a44ac27a16725abd6e06ae

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
