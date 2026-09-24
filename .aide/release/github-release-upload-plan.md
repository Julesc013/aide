# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=1c797d61f5c559b1e3424c71dc7306095e3438e2184351a3e02ff464c4b43fd8
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=b2d4dc7d5ef52c0bad0394bb6cf80d14dc1fa09ea7f93147c51d03f6473588f6
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=a8fcb7b34b4fc2968991c7ddd8897dbda9e605dd0178fea94d122c72e708b44a
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=36d36cdbb09d5b6bfc2e1804a67d6aecc5ad88e6951c239c0a360ceec9b113c1
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=dc7c0f485733b7fe78539ecc140295c2de4d76193fa22c89d74175884c63bd4c
- 6: .aide/release/dist/install.md (install_notes) sha256=db0ce8df44df9807b8dd137f9e2b0dada34ff95bcafd5b804d46bed0b824aa62
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=dcbce43079b9d56688c9a718468b3f63fc123be6d0f6a11f30555103d94cffd4
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=e5e2ba4893055be8bc19ce1c03ce25713efdbacbe005d90c14dd107af785caca
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=2506539a39ae65e7c783c1592e4cc1151ab0561aa6d7fc2a1fef54bf395ec747
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=4a1694df8586ec2643f012372d204ca255b8d7ce430c318eb0056085404298ef

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
