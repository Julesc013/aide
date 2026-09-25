# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=956b59a76d7d8d42cbeb83d776beab7cf096c4ff964314f4252e1e0531f4b4fd
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=4dd239edd4d52ab25bb4b41cb0eb9b756710894e5f4d0400defd9305d255606c
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=b5fc4a9a889aaacb6662853484b0e2e35cbcaa3d740f74949607005e8da9fb83
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=f60269f7f69e21fcee5e047c579d4da5b11189720e4c9f1ae6510184ed6e0437
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=72c47dbc06b37e2caecfd1d3919962275b559ab5be1e3173b2eda02c76375ced
- 6: .aide/release/dist/install.md (install_notes) sha256=7ce5608e0799b87bb94174be437f64c8ccd6203eeb94e3bfc6f098d852050226
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=acaee39b96e756689bb117c598e5c44fcc72d4187a963088e63ad4561a36999c
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=2edeaa4c5709880c91388fd98364c86b7c57e0da128fb83c82e7582d7bcc9ce9
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=888bd9f028357fecf3eba911156d3ebe5d9108495e43ad1e7f817d7bcf9db9b7
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=2c25b33abab6d71c5117eab67ae82768e930862e3df4a401c588eb9fa6571322

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
