# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=be9d0d77151c1206fd2119401f81ffb58bb62a38f8fb6a7dda4490cb7718c555
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=b444e546f3b7564e920389e5a9618fbf44a85a52f5676e5b6b7a82d33bab24ac
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=1a86606c235fb9dac7d97cfa5976676723ab7f27e65b6d5a2c17055e118e1e1b
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=6da9c1618d2e53a036ae955d7f94fe148394eb53a7144ad4673df5334e6e0a53
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=ebe74866b6017ad373e097a3c9da4a9bace0ac4a3ecee2f2953b73bc1a3dab3f
- 6: .aide/release/dist/install.md (install_notes) sha256=dd49b351e2f3e998579201a89c6f91de158c39a22220ed17dcc7811e2767c7f8
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=416870cfce568c36034590eb19b372994c35ad34fb69b3b75a2c1931b8fd387a
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=164073e1fa6e63ce8a52acc9b5dca73b3106c3bb9bf4e6a9ec6db7b8f60de198
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=2e83a2b3f71f5990b910d95006fc81b1ac88ea3dad024be9b0b6a2cee915ad51
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=612689cbca54d7e0945787e3c415054aeffc766a901e94c33ef5415c97473cf8

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
