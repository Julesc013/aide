# GitHub Release Upload Plan

- mode: preview_only
- no_upload: true
- no_publish: true
- draft_ref: .aide/release/github-release-draft.json

## Asset Order
- 1: .aide/release/dist/aide-lite-pack-v0.zip (zip_archive) sha256=6f6414c04721db7d91a17171a7062c69ed08ae498ad24f9345ebade9e0e9df9a
- 2: .aide/release/dist/aide-lite-pack-v0.tar.gz (tar_gz_archive) sha256=6818535c9b0330018834ad736a21e9471f57063927d92c084cedc11d73412f52
- 3: .aide/release/dist/aide-lite-pack-v0.checksums.json (checksums) sha256=b1ee06ee283c4a70b0ade96fbf1332794ea0e7f01c106f16c3195847dfacfc1d
- 4: .aide/release/dist/SHA256SUMS.txt (sha256sums_text) sha256=01c7cf01924842431473dc6534a936ae6cd708899d2f7701a58fe623ac9f6118
- 5: .aide/release/dist/manifest.yaml (manifest) sha256=de5438d8a85e41015f194dfe2a9de374572146cc004f6d0bc5d3389d5251f67b
- 6: .aide/release/dist/install.md (install_notes) sha256=b419951cd60cebc31b9116e3f178adef71516e9b46825b1185ef443781cf7fb7
- 7: .aide/release/dist/CHANGELOG.preview.md (changelog_preview_copy) sha256=4545f947e4e987c6c7b3964e144275d26f46902c4d591b701ce94400c34ceb63
- 8: .aide/release/dist/RELEASE_NOTES.preview.md (release_notes_preview_copy) sha256=08ea8ce62126cb699a2d042ca6417e9c3cab29ff91750599d250285d3b229bca
- 9: .aide/release/dist/release-validation.json (validation_report) sha256=a457b73f186db89c3fe444ba17864cfef2e0662ce5c12d808652cc24ed43ffd7
- 10: .aide/release/dist/release-validation.md (validation_report) sha256=aa0c336c3c2c0ded2747876f3517034f31dafd8f2a0f077274e0eb89ad649182
- 11: .aide/release/dist/release-provenance.json (provenance_report) sha256=7cfad84873ed6eb21a671a018a44db60ba872bbbd8e332e35e8ee96a0cfbee79
- 12: .aide/release/dist/release-assets.json (asset_index) sha256=48900e90e78aa44ba19539b3fd3ee226c3a08342446a6f5a46a1cdc7d0d34fb2

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
