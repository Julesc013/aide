# Release Artifact Report

## Artifacts

| Kind | Path | Size | SHA256 |
| --- | --- | ---: | --- |
| zip_archive | `.aide/release/dist/aide-lite-pack-v0.zip` | 721405 | `0855ef323500fcf4d1a8ce0a9a278a1eb194a2aa1772111d077ea22b05800922` |
| tar_gz_archive | `.aide/release/dist/aide-lite-pack-v0.tar.gz` | 478108 | `33a6efe051d097a35a5bbc9bcbda0b125d6ea0057bc08cf1a6547573a1cd4b52` |
| checksums | `.aide/release/dist/aide-lite-pack-v0.checksums.json` | 1200 | `b0214f3602c94f09355e22583f03fcd4e774d60933300516fb4d075d48f8edfc` |
| sha256sums_text | `.aide/release/dist/SHA256SUMS.txt` | 690 | `e775417160a9be7205302a4de33e3490e41357332f411adb656a69407cbc25cb` |
| manifest | `.aide/release/dist/manifest.yaml` | 1406 | `e8d5ad0b9e9bda6a70e2fc26835166404b84d0b0c7f30e0e6d6a23bbce3a38f1` |
| install_notes | `.aide/release/dist/install.md` | 1251 | `a1416ff3ce181b31409fcf61c9910c503e206e18375c50a8ab884b66b786627c` |
| changelog_preview_copy | `.aide/release/dist/CHANGELOG.preview.md` | 11440 | `2456dae7677bc06aca7791b57d774711a801e56e51148dd59020a7dd9afbd0d5` |
| release_notes_preview_copy | `.aide/release/dist/RELEASE_NOTES.preview.md` | 8285 | `49194f1b631e90f7ec02a84cb2a243243b3c8cdda815fb8cb1fc244ebacd1c0a` |
| provenance_report | `.aide/release/dist/release-provenance.json` | 1440 | `15b1dc9bb8901ffa95ff13233242a6cdb8a5b351e40c5b1448a23bb9e0d0fd30` |
| validation_report | `.aide/release/dist/release-validation.json` | 3418 | `746317110fd2e5cc0a6fcd41715839045d11232ce0b5e011a6658d56166528af` |
| validation_report | `.aide/release/dist/release-validation.md` | 239 | `df35747cfd0d9361cf1dfd5d36a185bceb5e4939f0f892bb7dbb97da16040aae` |

## Archive Contents

- Archive root: `aide-lite-pack-v0/`
- Zip entries: 608
- Tar entries: 608
- Required files present in both archives: `manifest.yaml`, `checksums.json`, `import-policy.yaml`, `install.md`, `export-report.md`, and `files/.aide/scripts/aide_lite.py`.

## Preview Files

`CHANGELOG.preview.md` and `RELEASE_NOTES.preview.md` are bundled as preview
copies. The changelog preview reports 15 historical malformed commits; Q47 does
not rewrite old commits.

## Tracking Decision

The generated local release artifacts are committed under `.aide/release/dist/`
and `.aide/release/latest-*` because they are Q47 evidence artifacts and are not
ignored by current repo policy. They remain local release candidates, not public
release publication.
