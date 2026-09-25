# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=e7e14b8e112ddcd762022c26b59deaa3aff1b49f69950fc2f4751e7fedf3e8c8
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=06852530d459271184022d17a11f514a8402351354683cae49899678100f0699
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=5203bc975892892f98b7f419353ac7a7f41024ad4f007969bb9cb6567f8e3869
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=19265bede7850adc5d7517e0549950fd84b9fab27fca74edf15ef05a177bc571
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=879b4fea6ab5e9b97c2b718a1a32cad535cd2ca7c78a35412d27cb3bf31ae81d
- 6: .aide/release/dist/install.md (install_notes) sha256=f7c762a448eec796957912aae17cc78100c8bc06b751482d5500ac2e77bb75e7
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=662f9a61099bd9e573d2aa85726264c44b0471e0a5b95eaf4853068a9ad80dec
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=7d8dd1c2ba9154d1ddfbbd94e2544097f20dc5ca9ea50455ba90fa89073f80a9
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=91ed927313e133b19b777271a829207e99645921198ac632261130920ba21091
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=6fb21dbd5ef6c7f3781bcaa92a89c4c03129ad671a7269ecc1743511bc88cfc3

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
