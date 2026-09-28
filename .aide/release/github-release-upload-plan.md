# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=8413a071db72ebcfef21923277ab8bd7226bb2b36a8836d2fc6977866ae945c4
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=739868e0f1c46cff1277d02a4141acb1ae18c5a4745f80563d2e24844bb98fe6
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=6b04ad3bed64075ac479295fe5613a63b0644a5b9afafb47e23943b59d11267c
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=a421300e818835b3c186804fdfe245fa9ba07ad3f1e0dc5d5c7b44ce79d7702a
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=697c0ed20929ce060d106f72ab669064e52c12b403305afbb88bbf3112332821
- 6: .aide/release/dist/install.md (install_notes) sha256=4b1cbfc21cd0a14ecb524ef63e48aa88f19e3cf036894bd4d766444eadc1970d
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=263cd047e995a967ea21c92c6442518f3cab35fd33675a2187b270f6c9da0c43
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=e65344ad19f7d7385b742046c0a4210bd22ca9d36843fe6cc8f7f74e159dc0f1
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=07e944a15ce9fda28b4161865b47abc80d15a1f2a315d1b92a88622a66c99950
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=7572536fe58ecbf35f837507bb9c38e46dea3ba2e376221985b2386181f6fa85

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
