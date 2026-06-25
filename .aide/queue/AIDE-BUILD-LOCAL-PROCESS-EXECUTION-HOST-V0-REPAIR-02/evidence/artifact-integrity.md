# Artifact Integrity

Artifact declaration policy for v0:

- one declaration per workspace-relative source member;
- duplicate declarations for the same source member are refused;
- different source members with identical content may share the same
  content-addressed payload digest while preserving separate source-member
  metadata;
- undeclared extra files are refused as `artifact_unexpected`.

Persistence is fixture/report scoped. It is not the future production
ArtifactStore.

Focused tests cover valid artifacts, digest mismatch, byte-count mismatch,
missing artifacts, directory instead of file, final and intermediate symlinks,
absolute/traversal artifact paths, duplicate identical/conflicting
declarations, distinct members with identical content, oversized payloads,
zero-byte payloads, unexpected files, and access-hook revalidation after a
member is replaced.

The persistence path writes verified bytes to a temporary file, flushes/fsyncs
where practical, recomputes the digest, and atomically replaces the final
content-addressed report payload.
