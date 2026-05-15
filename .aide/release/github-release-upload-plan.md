# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=5ea124268b5c0448c906cedab9d7d62d1424ae2749cd0547acad44964f610761
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=258c0ce9200c24c86fa237ace0df6ef58a9d9567cfb35956a464f56f48b9fc3a
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=d11f91599bbf13c39872b815b99a88063c50de8fcdf91aee76a09282bac2db06
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=60bfac6c8e912d1ad1f7929a55c820e2ef2edcaf340d6b8b9675402b1ee1291a
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=a63b444ba7b528b9528e7e0e096a505ba01c91aca700c026f76c883bc39a8870
- 6: .aide/release/dist/install.md (install_notes) sha256=6176f03b047465dea6919e8d2958ba0bb7217bc7940791f71cad7b45bef0458f
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=583d5ac82800450cd6473a4568a7c8c2111435413614969f71f8ae3de76ae720
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=51cc5473d4f14fab1ca5d96646c8933d5e9122eedf52f3e48c158eac52a06456
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=746317110fd2e5cc0a6fcd41715839045d11232ce0b5e011a6658d56166528af
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=df35747cfd0d9361cf1dfd5d36a185bceb5e4939f0f892bb7dbb97da16040aae
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=9394a6d96edd7ac64cbc70f4b7664d42f541c1a507ca1215a943ff7897ebc3c3
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=fca3e7459e9d47458235ab383a29636d55cb3c0e7f14d1383a12d92229daea0c

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
