# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=070c5d2c8bd36b4417dfeb91e60b34c3e52b46813a15455f19144dbb92ed27fd
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=b17ca0b0c44da360801c21795529af4d9b3dbd79024cee514e057227c1a5bf15
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=9a0be7027b706a52c83c5d94818b4e4f698b9a84369c5e47b7b08a0b2957823b
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=8a69ba6eea083d217fe03a00f417b59d5d5fe856db92f8650bb49cee7381a195
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=0b680d3e98683e12b2717a9c5d37617b761b40d5105a4121639f1ab3b00fdb7e
- 6: .aide/release/dist/install.md (install_notes) sha256=3899ad4e34397f262cc916230dd74964d401019820b95287743b3637105780b1
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=8edb41c9724a05a687f5707f3f1087533e0ae3bcb011b82986c97aa15c9eba37
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=3a29b38ca16e8615f65ff8884d2a206ee9b374c40d55ff9ff8eec2c65cb9c193
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=e0a471ce4f4879ce01e480c9a9a56e6bbd5b208f2cf973bf4fa1be9968553731
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=2beae63f3df285dfe87cf7bd7660e698e49d62fe58ba56decacbc2235b614ad8

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
