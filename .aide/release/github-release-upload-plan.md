# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=1b972fb1c96b1d673620e3543f079e10da13ec4fac1473379b8528294de25052
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=9b0a5bd0943d160dbd16059276c47a89aa573777de5df6ba5c2d19093757650f
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=0ee9ed3d59dc424d7b075bcb467ec2caf842a62362b4794f3c1d8fa1f9afc0c3
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=f111e433cbb31d8dce913a6e932b5dd0e209c5f3ef2981f56cb3bf326853bcc5
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=dbafe67bcdd9454a530a6f721ff0cd1e17a3d7e530a9a92b0237b3137ad36e25
- 6: .aide/release/dist/install.md (install_notes) sha256=c6964e83a0fbce0322fe09d31cf4998734677d845af95f50d8e24efe4e788038
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=e45b8dd6c1a0ceb9bbb8aaceececc0d212dd07709a433da7916d48764b4ac0bb
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=d8ea8c8d3abbeface0e8acfa51143b8f70eb176985e50ee829b782c87b5a59e5
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=5cbeb388a943e6168207bdac0cc04e717421545ff32a68acc2a29347b48c69f9
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=541ea57bcbe98fa57e757f4d67a8ae02795251eb2205824f5fac82b2e8c61dfc

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
