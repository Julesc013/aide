# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=79bab5d9a2f2aa157e5d4d097e79515429f1647501e90fc08057f8ade220aefd
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=c6909913472c259a54494d935600b582c2dd4261629677337758a138df35a987
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=417f4377600714b58e1d0ea8d4966a8f8579b09f809ef62bbe7113fba385f28b
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=1b9381129ee3040baac56847797c815a328bd9c338914959d5d3a91dd94a8fe3
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=651dc195472ce505006e0a4a0fc9770f4d4e91def58c513c8cd1b2be763b08fd
- 6: .aide/release/dist/install.md (install_notes) sha256=6c8a2a84209dc35328ff59b7ea0f872edb6b270dda80e4eea74ac9fb37f77083
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=88ca60e4969cf8b42b378a8fc2cac935f171f5b9f155ac5e8b34ac15e6359931
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=44d14b7a37bea68b7e842fb9d8bda2d845a6137159b24f487100c58f0a257a87
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=5ae193648f188ed2becb39896f23ff7528d83b177726ec9bd58d2f82e14d7e57
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=a0b34d25b14e9245226fb1caeb6109de9f90ddc9fa7307d52704332033129115

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
