# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=a9246ca97e10e1c5c9f2b6d65f1b175befe6a22dd7cefca3691fe44e9e82dd50
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=ddb629579650902feb8fb770813c8c8670e457e23b6983c5094982f37577fcb3
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=ebd24a05db9d197ba5770074d0c4ea111dc73b10191a4a0318d63df7746d6c49
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=5a169c6162ca9edc1d78e739ffdce48c6cc8f5a152575adb252d04af5a90a7af
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=530fc05a7b31b6b5399fd1079431bdbc1e3d654048d4ccab62b9e5b9c531beed
- 6: .aide/release/dist/install.md (install_notes) sha256=24b9886e650c24f90558faeec1ea12460c9441f40f5711b30c25802025c66b1c
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=42428f2cab71ae48399d9bb65bcf65b008fd07772162b7e2db52371315a16079
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=c00f27a85ffc87f5a40c925f12d68e535af58d42434b43f5398a3d96922c88be
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=496952a67fa3322933048ae200bbe37c3077720ee0fd29b209cb75d84a5f61e7
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=e34690058b3e835472f9212f56ac16f6b57ebf34cb005257800b8b8cf285259d

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
