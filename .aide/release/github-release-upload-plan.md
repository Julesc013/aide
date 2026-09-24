# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=4b9e458fe4a3c5f67f862de9c443ea195f74df7dd0bd2d0b69a4406562fdb5d8
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=65fc3f78f719244695a80914e73d535269d486a754e61b7b0a102969705f9589
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=8de0a9926de1432d95573309d77deb4a863bc3a9a358760cd6029b14ceeb5b65
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=422c9d2143750b4b868ec1c5be74e3075b43b2ce8a5f515ff8e43647419ff321
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=89eda43f57eb9d5102fb3a73a9561182da1cbc739a55e9d872712036e033b6ee
- 6: .aide/release/dist/install.md (install_notes) sha256=412437597dd73daa8953b92f40f3f0f36dd87f57a14d83dc4f2d64acbd7452fe
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=62f62ff9475c5b980280d954d9228fe6356102ca8f953c9c23913ff291ef0be8
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=9c07de3ab10094fb44bfb275395d2b92e1c02e2c093cad9e242556355629174c
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=d27b91fc133075a871210150223424b62cabb4e20990a804d3505449e977dc87
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=7b5a97d38335fa444faa9389ea5ccbcb04e50e239d17ed76b22befe814e9d88a

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
