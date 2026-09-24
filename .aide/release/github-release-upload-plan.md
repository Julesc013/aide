# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=1b972fb1c96b1d673620e3543f079e10da13ec4fac1473379b8528294de25052
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=9b0a5bd0943d160dbd16059276c47a89aa573777de5df6ba5c2d19093757650f
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=05eba5de1cc0a9c41824964689487e8f220be43c83652d11782b4caa9bc9b804
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=974d80d6a9a6b18d53a88efec4674f8a482ad1197d11143f0a2c63ad8031ffb9
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=4e0150db6be979c0f4aa1d5abdbd2ad3634ca7f27f6d5127639d1c820ec35934
- 6: .aide/release/dist/install.md (install_notes) sha256=9c62672e10a0da9381351639af8e561d862dbc6ad49960e3d33538dc23cf6581
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=e45b8dd6c1a0ceb9bbb8aaceececc0d212dd07709a433da7916d48764b4ac0bb
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=d8ea8c8d3abbeface0e8acfa51143b8f70eb176985e50ee829b782c87b5a59e5
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=868403336f111275229f8dd6af4e9fa4efa940f8e6760754c7ceb25404d832c3
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=458ae7c5261dff5e3b357aff9b4cfdf0109e1e6973bbdb88c4c66710efb7de5c

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
