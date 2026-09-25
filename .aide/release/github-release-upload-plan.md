# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=68f8b3cc07c6476999828577c59bdb8785d13509613d0351a617908c99fa784c
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=d0b424563ea7a85d207546b0e2b0d381641e046659846876adbddf96a954073b
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=e59bb98b95b95ad0d324456cb65b9de51a2c786933d5b74966836fe122048619
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=d4d330dd64519d3f47e64766ff4ceaa857a16c9cf097d1f84726ec20289ab5a0
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=fe6db9e8137c37c7aed859b229a3ab021b50235cf6db0f277dfa44edc248759e
- 6: .aide/release/dist/install.md (install_notes) sha256=69a902cb139bd3b7a6e327b0cfb9504f310f5e4e93f164ca6e7683b407e88594
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=e7a98808fc8b7ede1656fc5cdf770e8876886ca08086dd73901dd57e51d0e20f
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=9c7d559903ae79b75abef3efd9cdfb136e0dbea7d9520e705b3837d3449c0662
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=a1bbea8e59a180392f3243d20ddfd6e2f86ee3328f0f4f630fbdd3d1fabf877a
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=0f7a39b517e1543599c8d364d0a13a9bf05de9a7a8163bcf570a1600b5e8059c

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
