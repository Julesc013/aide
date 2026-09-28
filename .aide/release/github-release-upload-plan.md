# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=2a121ef77f9bc2cdf480991bf6d01775d265908aa21f25a738afdf847e22245b
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=3681768e6a0fb0e0393c03064b3dabb1baaffe75aaad3cb10d0fa0fa7fe29184
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=f3d9f49159b32ff479edec84831e67970845eb0baaa560fa02278c8df4496080
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=fee46e5741b4c0c8b6d271b0d1c70c53783063f0b218697fdff4293f7e0132dc
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=d38146d4fd584273c0d3f27d88aa4c97d59d6f8da163fe7c442203a1236c731e
- 6: .aide/release/dist/install.md (install_notes) sha256=de7b51b9006e8a126fa04e092182b7721ac38a82d6d44f5c74355a8c1feba57f
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=266d5643b16ca4aca24581280bbc37202d2c84db9ed0f453929c386c17489e3d
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=e55c41006f61c08046a03ca6ab9628b101a00b70e7aaf41bfb4915d8df5dff67
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=0f69dce6a20a83efe4d2493ed0f83e76cf9b0d536dcb64073ba13669e7f83686
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=7b6f99bd51f8dfb31bf9978263c3f97fec84bc6c8067a9cd1fbe5568cfaf0ba7

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
