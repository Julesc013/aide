# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=3f24c8e27e21c1884c866ad4faf15538a1fd53cb2905e9d9abe41f6fbe170905
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=fb855c0e88d26138014038ff3ed5c2c5f2fc26a57f08fafd0f842492a327e758
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=965db2435e40d479e89ce57e1cef96b20d0fbaf77f4e0d951e031b3338047f5a
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=fa821c3f1c68bca499846ebc88571ceeb30ce5f051cc13128011978fb2d044c4
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=3d45c31e2f66cbed39059b7bc510384e195fb7cd308bb98147f9e5cc1b4341c7
- 6: .aide/release/dist/install.md (install_notes) sha256=5d090c854fd44daa0cbbca7db8cea563c46ad86396765e32af3889b491ad0780
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=11e1700d29651d67f662840ff510d89c2cd53d0fd97754c0a621f36a81cc37b3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=458b6f900834140e058e3d2c79a610356b8026c0369f52fb3a5af405ca46892a
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=d38d595ba3990600c40824fad33d48a0f57639d3671297ec1657d565e9e35a4a

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
