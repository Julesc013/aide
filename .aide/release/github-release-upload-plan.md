# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=467b721bf03d8af4d035856334076ff74723a6d1a99a187d5dfba80ed8f5cad3
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=b7ee412488817528276a3b77e3edcc6bf26c337129b0043027ccd0a8aaceb1b0
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=5830fa6428cf7d7db4e1a3ce03fc5efda465dfaebae533843e12c17747dc4153
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=6f0f38259fd9349c378085780943fcb50746da7b759ab24b16d22ceaa4b270bb
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=02fc9901b53071c925271a156dfff99f207bf06dd0e24db5343461a5ff3e5275
- 6: .aide/release/dist/install.md (install_notes) sha256=87dac6680ff0bcc853da5972281100bd8aee5f445e1b8038966ab013accae522
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=983f3a861a41668ac54af141b42e6a2b2c26df72ff625fe12f299dddf3031149
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=a90c5353c3763a1fd44dd8948301f76e2f3b9ca9e827732bd897f091ed6e7573
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=7872f772b172036dd61413fc5bd992a1900cfa7ddda2065874cd0ff9503984d6
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=a955ee66d26913effb9036f7550a048f1f4a41126eee6ac228cb45c28152601e

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
