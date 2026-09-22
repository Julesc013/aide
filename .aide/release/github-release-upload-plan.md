# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=9bc5078fc7673e51fda10568bb2bc575d44c07de4889922178d7980819f8ff2b
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=23f6cb2cf5ba59866aceddd91f2b556da8c8686bdf40d86c631c016d0bde81fb
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=9df133f315620c20371c4d960100a65ec973ac13d35166a709c95c992667dff7
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=9fc1e0f2f197484e9f1ef8400c42741f24a30cc10061adbfadb1f0f38b37ad77
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=7cd2e48a6485230fc7302ffcc59433c604311dc0710773cf46211c41a3d668fa
- 6: .aide/release/dist/install.md (install_notes) sha256=3a41e4dab50950d067e492ad8c56af3e6fa298825a28015168b3d28c57a1adc4
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=fa94ab8f8c1a08931063994878e7566c56a23bba7d8bdac57e4c1aa4108c531b
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=2aa0e82298501316519a433a9453a1e2028365061d6c385452037a6b331ab6ab
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=193cdd72b05f0972a3638aac89393327e5f2fa31718c890300b71cc5b3cfa9ad

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
