# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=dfd344260ee39afc0fff833f266e480c3c59f74e083da986c5ed3685a25d61c7
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=57d382171974b92febe79f4a4f865dc8e386fe03213b36a2b6deff8a0c317aaa
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=0a1cddf3eaf2416288ecdb860001503cef2859827559031df402c834bd01f48c
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=161df94eb0c59b216e653d2ecea7eb05764fce61484f7cc7a94039e5186ab3a2
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=b995753581bc0663a4633c4eb0afe754cd509d8372ecf812c2ceac760d64e1f7
- 6: .aide/release/dist/install.md (install_notes) sha256=ffb7323d20bafd6c49236e9c0b4bef0679cb98f4ccb6561d31b4da00c104a20e
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=5597c7cf5598cbd3757c1617ef5b68ecce258669111bfdb64e5d0caa607f260d
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=1093f350297a539a5419963f95d1eb1ebc8f67d918ec427abefe09eae56b61f6
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=93d69ad1598a44403d079a745ca2f89a5598df6983e369ce6efe4fb2b3af29ad
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=53a6e2b8f3b5a9474ac30c76e3e8f2f363b185240de0cf55ce59ee6b280f813b

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
