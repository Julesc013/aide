# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=32c1f0ad5465809eec5d8ed64c801e8d3ca31c0fe5840ca41188a376325711f9
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=22101aa98982cf8b88d6a4540d814e9751095207535427a4e5a5fc3f36833044
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=eb98375d0ed0b91fe809d9729c7120c241702358dd10bdcb2cde9f668a861891
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=6a267a6253444f115906873986dc74377ef18c96cc3faebf39534e3a69c0b103
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=cae043cad6f05913fd02b2220fcf6ca2ec594dc6de7866e3524acac9c4021ce6
- 6: .aide/release/dist/install.md (install_notes) sha256=1419e96a778b2caf12a21a449d1e38f106fafceb92112780ce18fbb3fa1c4460
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=d809961de7600adb6a262616a657564c273b6ebd2a9502de19e87be5989d5dc3
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=d4119bd0ff7760c53f1cc3376608c3bfebbc4d3df06d37ea417f695f0065639b
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=a315baafa141c6847b43e6880fba8f853383e0addc0820f18f346c61142b44f8
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=607bd225b51071622ede5c15114390b9be3954b004e0bd4f6bfd1f2077080abe

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
