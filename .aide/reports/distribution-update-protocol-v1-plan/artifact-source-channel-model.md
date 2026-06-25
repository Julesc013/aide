# Artifact, Source, And Channel Model

## Artifact Types

- portable repo pack
- release archive
- checksum manifest
- provenance report
- SBOM reference
- signature or signature placeholder
- install notes
- release draft
- target-local generated output
- evidence report

## Sources

- local directory
- local ZIP/TAR archive
- removable media
- GitHub Release
- static HTTP
- OCI/ORAS registry
- LAN mirror
- enterprise registry
- offline mailbox

Initial v1 supports local directory and local archive semantics only. Other
sources remain declared future channels until checked.

## Channels

- `dev`
- `canary`
- `edge`
- `stable`
- `lts`

Channels are mutable pointers. Lockfile digests are immutable.
