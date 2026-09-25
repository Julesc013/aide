# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=467b721bf03d8af4d035856334076ff74723a6d1a99a187d5dfba80ed8f5cad3
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=b7ee412488817528276a3b77e3edcc6bf26c337129b0043027ccd0a8aaceb1b0
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=08f7d015e81fe4d87293257935ab5ffec0a2c9ebe706b36effff2cc40099ea18
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=da00d34fd7cf611fe80cba518ff8af174fcf514ea2f41ae6bc49203df35c9133
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=7bbfcb0587c491261f951a4d8e256ed1e7337245b3978ec6d8489ca7b3bef50f
- 6: .aide/release/dist/install.md (install_notes) sha256=ebdf282597d5bf3b46ea910b0c357f34085f1305e34b1c6f1b92e9ef57ba59e0
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=983f3a861a41668ac54af141b42e6a2b2c26df72ff625fe12f299dddf3031149
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=a90c5353c3763a1fd44dd8948301f76e2f3b9ca9e827732bd897f091ed6e7573
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=dbdda8a14b4d68b01d687e33e2b3f11f924a1807ff48102fcfd177d24974fd6a
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=a1e505d8f433d709aea9c7d3ca3d2eff888384edce1383348488506eaf8c0065

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
