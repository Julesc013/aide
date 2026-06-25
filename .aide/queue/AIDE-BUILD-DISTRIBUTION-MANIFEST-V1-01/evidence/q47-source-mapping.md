# Q47 Source Mapping

DistributionManifest v1 consumes existing Q47 local release-bundle evidence:

- `.aide/release/latest-release-bundle.json`
- `.aide/release/dist/release-assets.json`
- `.aide/release/dist/aide-lite-pack-v0.checksums.json`
- `.aide/release/dist/release-provenance.json`
- `.aide/release/dist/manifest.yaml`
- `.aide/export/aide-lite-pack-v0/**`

Q48 GitHub Release draft material remains publication-review evidence only and
is not used as distribution identity or publication proof.

The Q47 provenance file contains a historical local source checkout path. The
new manifest records that the value was suppressed and does not copy the local
absolute path into committed DistributionManifest reports.
