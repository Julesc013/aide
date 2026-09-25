# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=33cb8c061e32cc82853948bdf7f43bf750db34ef1da395a2ce3b857c7d532e90
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=bcafe450eaf7ef49d16a3b446bd2347fc644b1a675d1a304cff131619bbf99db
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=4b7ccf96faaeaa366a60a13739a60647773fce7bcc46743dc285987e516c18e7
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=3b6275abea38a7667aa7029410b756ca8c869f9662b2a72222ea318d7906937d
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=c63e90f1bbd83ac03bf8afb88aa041646f6a97e9997e2e9bf6a713989a6470ca
- 6: .aide/release/dist/install.md (install_notes) sha256=6872cb2ba0654c4e9a3ead6bae2c937d77e67764fd1dff82fd8e8cfa7a27f654
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=490dd3020f738e7f6de67c96135de1c9f16838e8a3c9424c258781c8aa6dd6e3
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=310ad0ac101fb2935bd768d28c9eae9af28257ad3cf9a35fa086c6cb73a1a075
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=bd9dcd335593c713f35032c6168506391084574bb9782465b501b3edb232cdc1
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=0e5bf47abc0689cecfbfc10265f502796e665286e244fc2304b6970622dde385

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
