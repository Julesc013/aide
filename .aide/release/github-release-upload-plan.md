# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=71db1f91922cb7ac010a40e2d55f681ec85624bb721917a44a002fb73a4429ef
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=950f24f4ea5c4027abc0f26e93918a748740c4560c326553f3d89cbdba5b688f
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=ba90daf2eb87b5679f4b3b62fc7be9a0a2fdd9aa37803b22f9cf2342cd2b0e28
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=461ba7d6d3a82259233b892af686ad890492a4131689846e34e7e64836e53e37
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=0300e72ec735ea781fe83a7cceeb80e7e351d9b02de34d2a1010c5d105d6db8a
- 6: .aide/release/dist/install.md (install_notes) sha256=90aa739ea427d9780a74a7c2893433cef1c7420416baabd6c452bad5cee33ae1
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=c66a28dc1b1c7e029e0f70ca2b9daa3463cfd7c3f9314cdb4e1062baaf4c7465
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=72bba722d3d1de2cb87f0b0fd6efcee2da73f4ba4bb50ebf89ea60f5cd37f517
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=9b8c478722dc16275ff68ccce9d97210d721cbbd8c9b073541b4b2f929bbc520
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=868334075d7d128ad092862981edd2a972ed431c5c891ce2a91bc409715e53b8

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
