# Artifact Store

- payload digest: `sha256:<64 lowercase hex>`
- valid payloads are written to a temporary file, flushed, fsynced where
  practical, atomically moved, and rehashed
- duplicate identical payloads dedupe by digest
- digest mismatch fails closed
- invalid digest/path traversal attempts fail closed
- metadata is recorded only after payload verification

This is a local fixture artifact store, not the future production ArtifactStore.
