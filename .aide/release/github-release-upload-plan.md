# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=298b4e7b38c125540a6b04c6405712ca665b895ae64d0fa3fc95ef3a51d59204
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=d5a755716cd862147fd7d13a09113493800933c4b0c5487c8a52f8ef28f791f1
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=a8eecb9f9b379d6244204fc65c7e4606ff669b1543408181fca72fb766d8b552
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=6d1c7f5761525e6e5adbb78780174f264e66732231c6b1e3efe3912de362cd15
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=2c17af01d32906a99b587ab5797ac859c91e69fb20cc7ea5015975f81ba0a22d
- 6: .aide/release/dist/install.md (install_notes) sha256=4316672cc9aeb35adcb71a0a6c6aff67ff0371180d2698a0d00e5a7d381ef29d
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=65b99fba2b0bf28ac37584f2c79a3f7f0547c78fb4126d67be04886a2cbb1a40
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=f9cbfec83f0cadbd1dde1f51f23caf2cd0aee4b9f3f3404b2427a0ce335fc61c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=9e3797fc6662e173b3f5fb4806b118bf22897349a2a96916bde39449fea7c252
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=df35747cfd0d9361cf1dfd5d36a185bceb5e4939f0f892bb7dbb97da16040aae
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=3538f2bd44f07286c2395641f7a28e26e84402297f644a8631307ef500ec7b39
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=591b57198b678075443b8b6d5b3107b722d2285f3c8db04801392af2055920db

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
