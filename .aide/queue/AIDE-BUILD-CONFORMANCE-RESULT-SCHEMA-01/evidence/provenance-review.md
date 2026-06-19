# Provenance Review

The result provenance is recorded through:

- `result_ref`;
- profile ref and profile digest;
- subject ref;
- source refs to the accepted ConformanceProfile and CapabilityManifest tasks;
- report refs under `.aide/reports/conformance-result/`;
- source artifact hashes in the projection report.

The source mutation sentinel reports `source_artifacts_mutated: false`.

No branch, worktree, target repository, provider, Gateway, GitHub, network,
release, or runtime surface is used as provenance.
