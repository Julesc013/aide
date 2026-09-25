# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=8c4fbef71470954c64dbd09e181384a3fbff0ec997a799ef197f0f6cce1e07f6
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=11c95b9c10355cb617225472cd0c72cbf8a9bbe62671d6926bd28512967aa34c
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=1cb711c1b2e4a7787d016c1474670f8f532560490b203f694d413be8143d9ba1
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=740d6c32b0e2c4bc8c757df472ae5e7981597f2cc5eee1779626d9e933bd6389
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=e4d11aa458799d35d6ee66fc195de174b955927d9913de2cc69f7c405656869c
- 6: .aide/release/dist/install.md (install_notes) sha256=6e6f21f90ba86ec27abd87501ad30c1eec1b2fafe08b7559b590f8d7f91c7071
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=f7b97ad091ff1b9f40fabb51fea9409de38ba5a7f726ec3b6912bd0a2fd7169c
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=222a04b829cac70cc75860df720938453c1c9b6247e6480615b95ff4815fc42b
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=f461068624899f3d2f5ad4a0507c52b97348809a067ea3b73086334fe7b5b94c
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=77c865fe1939e994b686acd30e362b19018a11f2b82b49fd4bb221f970d519c9

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
