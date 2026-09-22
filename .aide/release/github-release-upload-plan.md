# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=622224960f882e1055995c2a9ae6c408f1ba3f8ec242bfe30a5353be781040f7
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=9c16ad304636badf26f9ac1029e833e548181fa411e119574e3cd71d683a4ccd
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=0b952ebf7e7da2d08d8b1f0e884cbafacf62ff68d65654a0d02b23a0e14c546f
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=59a7600bdf88d25a7b4665369ecc9fdfed32f4fc8dc335bfca99a43ea05ea0a7
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=92039cc42f760f20ef7c01de4cb47bdffc880eb1b08d50c6adaf4e73b4c133e7
- 6: .aide/release/dist/install.md (install_notes) sha256=c30a5d82bdfdd0e7329c051f2cefc1847aad4442c23722a4fe9558191439513e
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=a7d49c6265bb2132d096817094ce44ca886e6ded573fda40367c0ea4d1c64451
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=46e5f34c74e336de105162d5b9fea0688d1ea740f55a11be805e06d3bb05b653
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=47be2b4546ae2264d854b8b2fdab018e3baf6ad503296e1066dd3cf58fee1a04
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=4b0b0e521f386065c323b01c32463b12a2ef8a5d437b65f02023b21d28298fd3

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
