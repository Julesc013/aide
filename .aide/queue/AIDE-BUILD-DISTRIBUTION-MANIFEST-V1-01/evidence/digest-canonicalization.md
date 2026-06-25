# Digest Canonicalization

Implemented digest law:

- `artifact.content_digest`: SHA-256 over raw file bytes for files, and
  canonical directory inventory for local-directory artifacts.
- `component.content_digest`: SHA-256 over canonical component payload including
  sorted artifact refs and artifact digests.
- `status.manifest_payload_digest`: SHA-256 over canonical JSON with the
  manifest's own digest fields blanked and signatures excluded.
- `status.distribution_digest`: SHA-256 over the manifest payload digest plus
  the immutable sorted artifact digest set.

The validation report confirms reordered component/artifact input keeps the
same distribution digest.
