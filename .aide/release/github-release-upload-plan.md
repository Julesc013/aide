# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=5210c9fb5d1113799f54318e1939752920f2bde697be843c0b1558611ccef497
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=dcc10541365cdcaecab4241b425505cd55e7c86ee94977a8fc6a3b1a0845cda5
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=1d0f1245857b5e9bd97b55a7e3229fb621349d4e8d38b1c9690c3d0c4f2b01d6
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=40e087a98ffe1cb13c2828b57fea98bdd9c5ba8899d9b87e3941cd7b5ac89877
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=27af8f430a2ab36f0fa476d815409533b6988ea706a0b2cfc240d29028e14e38
- 6: .aide/release/dist/install.md (install_notes) sha256=3be30edf49a38436baa3d9e81183bbb4bff1e583fb8543fc3fb22f5638a3c9c5
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=1b5fd5cb1df7ff0a99a29b51320d8c1ebda03974c43c6f2c657faf687b00fe2e
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=15d4e3a49e024385054d0550128b21c80d12dbe1b1997e835f7114cf87fe17dd
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=5b17ad6816e236ad37ef1d05e4b38c1e65ca1745c88c185e005c3286a169370c
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=8c2f65632f63d4a573e1566cc1dce16204cc5a6d696f5908e349d2056d2a9e2a

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
