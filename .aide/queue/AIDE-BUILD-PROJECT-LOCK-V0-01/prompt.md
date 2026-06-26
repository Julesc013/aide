# AIDE-BUILD-PROJECT-LOCK-V0-01

Build ProjectLock v0 as the target-owned exact selection of one accepted
DistributionManifest and selected components.

ProjectLock must bind:

- accepted DistributionManifest ref
- distribution digest
- manifest payload digest
- selected component digests
- selected artifact refs
- dependency closure

ProjectLock must preserve these laws:

- channel is informational;
- digests are authoritative;
- required components cannot be omitted;
- optional components must be selected or omitted explicitly;
- dependency closure must be complete;
- unknown required features fail closed;
- unknown optional extensions are preserved/tolerated;
- target overlays remain target-owned;
- source latest outputs, source reports, `.aide.local`, absolute paths,
  traversal paths, and secret-like paths are rejected;
- lock does not imply install, admission, authorization, apply, publication, or
  target mutation.

Stop at `needs_review` and recommend exactly:

`AIDE-CHECK-PROJECT-LOCK-V0-01`
