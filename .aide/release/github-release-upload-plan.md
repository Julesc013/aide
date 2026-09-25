# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=949cfc24ac261f2db520e8c1c4e80f46d9f9ac569ae6c6d5ea62c6e0c31434ec
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=26081af25c94d8494542b120ce1adee4df27710e089f65f707daecf8db679c2f
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=ae5d61324f8a78db2e170f7379661ee4b9f696afd889d6bb6e1bdbb126dbdc87
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=a145cde2ac9b4fd587b6646cba5b5fb9d98615bbd2fc4ccbb209b1bc45a3b2d6
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=6e57e252a78dd8a08383394a7aab19836e27191aed74aded888fcc7450d92fb1
- 6: .aide/release/dist/install.md (install_notes) sha256=f2d8499ebc7f1a6dc5b092a1b1a3ed94a8c74989cb4ecdeaf5abc111dd588a91
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=0d60002888bdfe5253350dffc725b6b0fda848c06e51a310f999267e42d7c1ed
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=dbc9dfe95622dcf84776bd78482c4703cd88b1c9c130b7139a4ae87b13cad758
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=19b0b4a18ba67d7288c3cea65ccb208c40c668087c626e9c374c3d5488d2181c
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=e3644196e4f4021650ab5108bb8d17104f4079d687bb612a1fbe3a647b3787d3

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
