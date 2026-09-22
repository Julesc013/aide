# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=dfd344260ee39afc0fff833f266e480c3c59f74e083da986c5ed3685a25d61c7
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=57d382171974b92febe79f4a4f865dc8e386fe03213b36a2b6deff8a0c317aaa
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=493a7303971d94218d7081dd30a7f5fc31d5bb715221df86d7793e5d88f5fb92
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=28be2162b024f00122040b0b2a6164be4570c8c5cf9fea126ed952ecf6b7367e
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=393becf195f2baf8d4026d3a2f9860e59c117cbdb8aebf39c150a3af65193b4d
- 6: .aide/release/dist/install.md (install_notes) sha256=dd326baa6408360bc3c96b0c5a17a2718dbfa3222c67af0992599bfcbaa91e85
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=5597c7cf5598cbd3757c1617ef5b68ecce258669111bfdb64e5d0caa607f260d
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=1093f350297a539a5419963f95d1eb1ebc8f67d918ec427abefe09eae56b61f6
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=ac3218cb9d04de920b9ea15a7cfce686483d252103cd023abd6014ee9225fde3
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=37b6d4e4c7f5106030cac8829decd81fed05f89641c70f5b87efdac0c363932c
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=197bd8d0e66cd203d32f59f35c559ea6f7bbcc5a3ae35db515b3da0ef937f393
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=f71b9161c9a299f2a6074864c83360d8d8c47b0d498127447fea32394b36d88e

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
