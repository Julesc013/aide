# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=33cb8c061e32cc82853948bdf7f43bf750db34ef1da395a2ce3b857c7d532e90
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=bcafe450eaf7ef49d16a3b446bd2347fc644b1a675d1a304cff131619bbf99db
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=2df9ccebb61760ac75dbe2822157ac81cd4ef46dd6d55c5f58875d5cab521624
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=60a139d8869c8491b8084f710e3fe7d49067f5481cec5a0aebb32d084a11a099
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=cbeb8626529399039df51a0495a115fcb7ef52120c8fac4e012de46e412dbfab
- 6: .aide/release/dist/install.md (install_notes) sha256=11244a5fc09b46152db5114fb75e3d26124acc3783cf2cd624a12c34207b11eb
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=490dd3020f738e7f6de67c96135de1c9f16838e8a3c9424c258781c8aa6dd6e3
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=310ad0ac101fb2935bd768d28c9eae9af28257ad3cf9a35fa086c6cb73a1a075
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=d00b19a2811a370c47c83ffadffc978007531e98c2be87d3fa81c41d81f124b8
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=03ab8fb9b8386c80cc871d81a34327a2947ea99349d97b6a339c4e6a6db00a95

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
