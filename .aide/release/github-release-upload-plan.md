# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=1452ae29333e9ccd69f02a29c16fbe9d7dded58b03703de1a5a7c56db91702e8
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=57575e417ac164594d83967f9daf5eb8be2976d4f678c2d0a59d0bfd8d8db114
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=93dcf9a312ffa09cb77d83117d08a5af637895b47f30cfe83e31036f64bd6d73
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=3e91c30da8b70dd458b75cfc3c693af87f822af5f24a75dcda555aa2a6cb8172
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=cbfbd6d29c9ab65cd768dcaf03af4439802573584cb1cc8701237563df0becaa
- 6: .aide/release/dist/install.md (install_notes) sha256=f8a6aeb5a6066abfd48ae3345bcefb08b26c6567aaa84e6577ae68dba4a82de7
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=d01fbfd9f5e4766338df3049b3089d9d923566ba87adc7bb45e27016799c41e0
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=043d0556d26046f2bb0a4c446f2cde4d389cf40fe327e6515c36ede50ea9d1fa
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=4825087358ad220524f9a637e19866e444acae99f4b880ad2693e092fec49e70

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
