# Digest And Validation Review

Independent recomputation confirmed produced selected-source hashes, record digests, and projection-index digest, but found material validation gaps:

- the final `seam_bundle_without_self_digest` does not match the bundle after `validation_summary` is updated;
- corrupted `source_snapshot.snapshot_digest` and `content_digests.source_snapshot` are accepted by production validation;
- a valid-but-wrong record `source_revision` is accepted;
- a second singleton `HostCapabilitySet` is accepted;
- dangling artifact references are accepted;
- wrong semantic ownership is accepted;
- forbidden mutation capability IDs are accepted when mislabeled `read_only`;
- duplicate event sequence values are accepted;
- arbitrary diagnostic severity is accepted when `severity_valid` remains true;
- invented refusal projections are accepted;
- removal of `HostManifest.spec.host_id` is accepted.

These are bounded repair issues in the seam validator and generated evidence, not a reason to broaden the read-only seam into runtime or mutation behavior.
