# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=03f1736328163aec1a8a4d27aace9ebf8aecf71b69792957d3d24ec53fabce39
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=8e64ecc0be58f798fd44b5556e33511f6e641d908bb96a673afdefc5b233892d
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=89d02d7270f190b7c027cf899a43f0592523bf81541e708fab72347a8a166f71
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=058cd24fc36177efe6e0d6d69f108347013f12413084536ea70d11172badc98a
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=5f3a1d9c72154047082aaee8757991618b344da2a623c6cd110146f0d26890ea
- 6: .aide/release/dist/install.md (install_notes) sha256=1bb2878883cbf6448a9120a8c4fb5894b789643338b48c16062e80e2748b20dd
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=ec64815395429e62ddbc73cefe02c5111ec94b992e41703adeadf815d713f2f5
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=993ad7c6632783669510656b8c61eeb96cf500a3a0c5f871dc2d7b3a5c87f250
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=c9c13cb4cc0494e53cfe14de363783ea167758d4436b063e50aa51dfc1bb3d25
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=8188e2e14babea8b61991985db502ebd1c571c4d6fca321659d5258a9713a771

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
