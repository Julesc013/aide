# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=e0155fc838ce6ef6dc192ab1b46edf60517dfdd63d8ca2354a50e1c4b8fa8280
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=126681bbc1fc8701700a706cf2a448fee7109913d1a109e20a4a072198dfa47b
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=b3bddb6f1deb044011661d8e4dd56db74f6a625dab43d415b1386679be190a18
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=e179fa72cc3a746851b7ba0d14877250a650d38c21c7a4833fcda3745624a04e
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=a49a6d4d2bc3da7163926c041a7b59748bf4cfdfb39fabfec0f5d4f41e84c0dc
- 6: .aide/release/dist/install.md (install_notes) sha256=e09b6da1557fbab93e89ed193c06d6ff7b93c0fbc1eb045992436e1314156138
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=a28f3e92a16c7560a3b07d48fb23daa5ca4d48e2b5fca291ea55b585e4ed7a8a
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=41b227fbd12910108177fff26f97152648dbbb66b97de9206e4c443c1296f4ed
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=cecc80c7b89e53e62f98695705ab44443269e32fb8e724a9c3c393f9fa9675ff
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=24d4449c698cf008fb88890d16c73b00583ec49fb658a283efb7707c16231601

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
