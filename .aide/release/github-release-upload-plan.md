# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=c526104fef6e01d27d897203a7739420336314d8f71df6d3474396b99dceef84
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=a89d07b1b148aba9f77a82146462761220804f1762cb7c8837268cf307735c33
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=99581588606588df7f0c3a94b510eff15f5585de0cca504b86c267d5cc340e9e
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=dab15595b1e4b4628e488152f075441622412af5f78c05ee2beb08603209dcfe
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=d35aaf330c57de709516bc26be35b17144d5a58622b0d9b441f7e6bafd0ef711
- 6: .aide/release/dist/install.md (install_notes) sha256=00631aaddc63b85f09a8d43ef081085cf90cb6dc7b2579a0443dc77b5b1a7b7f
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=f5af8a38b86e629efba0d68e6fee0bf849cb98ad213445a2c61e6512f8006046
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=1eb194be68b68fba0e1531830643f80ae8e0e2d9e9851ac6d9606f923f51eb0d
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=7108bff2f73cdcfee2e3d76c2df0f2a54a5bd07564773c494f99cc4d9e8414a2
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=46e535f96fd73e91b01750399e437dc44a9b74a358c78795ccc4bbf31400c50d

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
