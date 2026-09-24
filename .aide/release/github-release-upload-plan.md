# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=515817522aba08281cb7f61a55185fbdc315b861d002d2008b3a3d94d7235411
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=c5def15fc3920d25aad095ede0ea4f39966f8cff2e082c4ba06facb5414d5bbb
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=5b0a0753aed556611b2dbd643a4905bacf492c1f0f475191443e397a7d7cb795
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=4304c274efc0c2041f88dc914274819b89f04c4ef6645eeed84c747fd231f8d1
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=1b913456ba7388e447980363cef14a0a6426346e03866ae4399322eaf478c588
- 6: .aide/release/dist/install.md (install_notes) sha256=65dd96c8d6e162278ff9ce26aa91b7b3e72fd978d79989e76a26c94c7817b9b2
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=5ba015ec96f7b72c590516856e6297f0c1daeb03f10c655162e85bb72b1312b1
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=5e27dccc8ca665359949e39a61d7133ebf7b1aad44b8ffb17eaf42b135f869ae
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=eb9d64f53b1e7ba3af1fbf32dbbf6e0a93dc299259c4950f6707e74eca78eb40
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=dc62cb58059fa43afd9603b15f6f78e264954d1f79d63b539a59b725edad1ea1

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
