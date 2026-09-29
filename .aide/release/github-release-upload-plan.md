# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=bad448be72939d8b994bd507ca0b0329e11a9d4086c30c0d9b65ebcfd9611357
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=855800dd9d4ac6209d89eaa46ce4152b9147688e10a624a3337f028671633404
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=c6ce208eb76d04d079293441e53f856a79d7463525ca7b1de553ff164ec97ad7
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=d37c08fd37dc4147e4b2f7843f85a4ade5ff797a1b73791610112325f46d9efb
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=8e9215afcfb7789d125a349d8bdcbc8f99d46c3db26c04861c8481318f1a0728
- 6: .aide/release/dist/install.md (install_notes) sha256=a28256b04b9fa69c65687dbd5f4a6c8184b3f5ecfe837b874765a4572b1d3173
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=873060e4dfbb3268324736364544bdb38c13dcd84007cd74e599d125a3cbc701
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=8165cda085595ba3a99a4c6ed25685deaac0a668914cf21d23b56329eb33c597
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=dd70904576ba86ce0dadc630e42d0e8f9b49b93b62c584257e68b0a1cbcfca82
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=2b63bccd4c154ee3bb6daee8440dcf3da3ff9d01f033f8307f9045405db9c462

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
