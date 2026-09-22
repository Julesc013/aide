# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=48b3a4a4c3f6e443cc16919b5ac7c57ddb5070f5d50bbb80cc4b559ba3bf0355
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=105f9fd774f04e8a9ef3cf0bb4dc2e5862f9f40121e92af68e1158b23d6a88d6
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=99c952999cbff48fcdd5305e6a5d5ac370350f3d8efb5cf459e294f97990c345
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=1461007787072e4700a1ffb767777083c7013af9631cb5a6260f8dff9f4ba586
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=51994dcf91e2401c7ba66f1ef638ea9af11acf55f1d6ca1ad463ba4b708f3e0a
- 6: .aide/release/dist/install.md (install_notes) sha256=5e286819f75bd9ffac0d14780cbdfb0a3ca4e47dabfcb75562cbb8552bf94a8a
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=fa94ab8f8c1a08931063994878e7566c56a23bba7d8bdac57e4c1aa4108c531b
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=8795443d5e41dfaaf02c64e151ae9256f9170d242e6174d3a0feab28dbbc53d9
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=36095a6eb4bf3f90c2cc1f990d8979ab4ff82369ff480bc6b0b94a2230e314e9

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
