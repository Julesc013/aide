# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=af8bf103353d72eacbbf1f2f28cea8cef1f11ea0d942872c57f76aee9725a7ff
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=f0111bd834eb1aeb0b5b0ea70562ad7e1294c04dea8fa0bd83ab9be5cb294725
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=e269877184c63248f3ec7c550b6dbc2a6bbf7ab7777dd7f2be9858b7aefd61dc
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=69a6f01fe006d89b6d8ef7b0738c277a8e9803c841671b0c648d86be38b7f482
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=b48bcd3a7a33779ab74d633755d858e5cca7c6ec4b7c72f24c9820bdd56223e5
- 6: .aide/release/dist/install.md (install_notes) sha256=a8671664ea0d2731bc20c740a06bde16f886f17ca71695594d2470a38d92d6f2
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=81bc162e3f9995bf41a1d168a78f3ad1086a1203c692ae5368620a747d182c05
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=f9c9d1c3a9f67dba9897789dbaf5d847cd904f833377338401efc7b0c7aec1a1
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=0352f5786685c4bca2b8a8957714c03dcd54f3f2f72da548b4439bcb5c4b557a
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=e89fe8cb0dbf7b24e23e4481165755c6065010275053cbc7a6f97967a5276958

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
