# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=af8bf103353d72eacbbf1f2f28cea8cef1f11ea0d942872c57f76aee9725a7ff
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=f0111bd834eb1aeb0b5b0ea70562ad7e1294c04dea8fa0bd83ab9be5cb294725
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=d805e9dde1984b580eadf3151ed58e8e41681e154240f976a4b8d81f42edf28b
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=032f4192350fac4f66b08f2d61a3ca9dfa7412868fc20e07d66b452165d750ea
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=4e1a46a8b7f5f43eea14fc6e835715f33d992734eef70beaff1b1bb95f3d5b50
- 6: .aide/release/dist/install.md (install_notes) sha256=fd723ca751120d72a074a34166b9cf6d3178a14f61018f16d96f78d0548bcd0b
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=81bc162e3f9995bf41a1d168a78f3ad1086a1203c692ae5368620a747d182c05
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=f9c9d1c3a9f67dba9897789dbaf5d847cd904f833377338401efc7b0c7aec1a1
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=96440b8513a58e34e2d3e73cbc48743d65b8f187a78e48937203b3634373e30d
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=1448e5c6dcbb258c0d7f727fe4103ca95e79a50e4af4b6a67d776501004a032f

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
