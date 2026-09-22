# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=9bc5078fc7673e51fda10568bb2bc575d44c07de4889922178d7980819f8ff2b
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=23f6cb2cf5ba59866aceddd91f2b556da8c8686bdf40d86c631c016d0bde81fb
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=9b9bd22b6d9a6562e39c62f5ca81df9f96792033b46029509c7476ee21078455
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=70769d5c363bb3c9ca93ced06a3183c270daf2a721d8a96c0d156ed90e32a4a5
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=33c86efb760d4c69ef7afc55a8eaf450071b987186bb5c07099414b9575b4be4
- 6: .aide/release/dist/install.md (install_notes) sha256=b22af39898c2bea2e4ceb259da2ae712161ac14915337257af5127530c9139dd
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=725d7aad7d6f7385121ba706fedf28675c443fc7a7a88bc7340d12fb724f55fa
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=774a75827477d5e85f6a9659c74e0c85dc035e147f5e94161c843338077b259c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=c42acc5280fa5f2d1d00a18b2a362bf515ff3d63e411843d2d12ce45b319e37a
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=0d1c0de0bf81fcee2a59ae1c14d486c5326aec3fefb2c16e04cb60e4d41b68e5
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=b57eebb15e1a3a6457bcf9babce297705ef094c3bd8748e6cc0f10e5bdfc4274

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
