# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=1452ae29333e9ccd69f02a29c16fbe9d7dded58b03703de1a5a7c56db91702e8
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=57575e417ac164594d83967f9daf5eb8be2976d4f678c2d0a59d0bfd8d8db114
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=c76ff400984c48982b4051f2214dd0551beca399220cb1fa3643809cea8c5d7c
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=6f14df8f7a370599bafb6ec93400a0cf9e6f7c1e20675dd22406518ff15bc638
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=cbfbd6d29c9ab65cd768dcaf03af4439802573584cb1cc8701237563df0becaa
- 6: .aide/release/dist/install.md (install_notes) sha256=f8a6aeb5a6066abfd48ae3345bcefb08b26c6567aaa84e6577ae68dba4a82de7
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=c42acc5280fa5f2d1d00a18b2a362bf515ff3d63e411843d2d12ce45b319e37a
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=043d0556d26046f2bb0a4c446f2cde4d389cf40fe327e6515c36ede50ea9d1fa
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=0fa339c775ac3c2c9c06c71294c71fe6d1305e896c84fd3681b7353c2fffa3f6

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
