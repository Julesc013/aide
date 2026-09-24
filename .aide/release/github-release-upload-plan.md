# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=787759eda0c0d4c159106b0eec271eb876a099133d462180a50c06a2077d89c8
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=437fdefcf524ff2a7d7918d34554bb84f18df810a4aaa27465019260182da435
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=52581f8293f1ad6c6290989f53531aefbd19d5fad3606e8315c0451ddde2eb1a
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=6c94e6f1908920f4851fbd0d0bdd17c9be25b7c38dfd88b1c372683110d4a561
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=a390925c95ee699d460653d0e1e9535ab99ae6b1c035fb8ce7035e45f10f8546
- 6: .aide/release/dist/install.md (install_notes) sha256=169c8d8e49d991cd25d2dcd2528441cff1c131a66e9043333d33d3e6cfa3b126
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=27424d692791c852fc290c07dca165545e4f74f0b0cc95ca931ce0fe75505731
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=95a114721e2f4d7551d0e374378cbec86f5f57b68cf2201e3357d3900050a770
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=411f7416dc15431e0035b2a9872bd694e1f103009baf2e58e9a231286da68310
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=dff4a14e30b70c87c7ca1aa1fd5d8a0e74b52b5d8f6577c6c3b670b135048174

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
