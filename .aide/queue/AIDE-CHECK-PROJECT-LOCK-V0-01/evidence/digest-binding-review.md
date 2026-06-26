# Digest Binding Review

The check-local canonicalizer removed `status` and
`metadata.selected_channel` before hashing.

- Recomputed ProjectLock digest:
  `sha256:a872bf91db42a04e3a9ca5e7db1fe23a5d81cf7eb101ece326114a533727dc57`
- Reported ProjectLock digest matched.
- Distribution digest binding matched the accepted DistributionManifest.
- Manifest payload digest binding matched the accepted DistributionManifest.

Mutation probes:

- `status.status`: digest unchanged.
- `status.recommended_next_task`: digest unchanged.
- `metadata.selected_channel`: digest unchanged.
- `metadata.project_identity`: digest changed.
- `metadata.selected_distribution_digest`: digest changed.
- selected component digest: digest changed.
- policy overlay refs: digest changed.

Disposition: `CLOSED`.
