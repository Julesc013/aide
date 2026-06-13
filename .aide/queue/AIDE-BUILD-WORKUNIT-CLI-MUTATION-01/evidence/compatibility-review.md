# Compatibility Review

Backward compatibility preserved.

- Existing `workunit status`, `workunit list`, `workunit inspect`, and `workunit validate` still pass.
- `AIDE-BUILD-WORKUNIT-CLI-01` inspection still validates.
- WorkUnit Queue V1, EvidencePacket, and ContractEnvelope status/project/validate commands pass.
- The accepted read-only capability remains recorded as `minimal_workunit_readonly_cli`.
- The new mutation capability is additive and labeled `minimal_workunit_queue_metadata_mutation_cli`.
- Unsupported `claim/run/finish/repair` remain unavailable and fail closed at CLI parse time.
