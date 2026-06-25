# Protocol Compatibility

The manifest declares:

- schema version: `aide.distribution-manifest.v1`
- kind: `DistributionManifest`
- required features:
  - `distribution_manifest_v1`
  - `portable_release_bundle_v0`
  - `sha256_digest_canonical_json_v1`
- supported source kinds:
  - `local_directory`
  - `local_zip`
  - `local_tar_gz`

Unknown required features fail closed. Unknown optional features are tolerated
as warnings. Required migrations fail unless explicitly recognized by this
slice; no migrations are supported in this first build.
