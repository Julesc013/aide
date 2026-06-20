# Compatibility Policy

- Read-old/write-current is the default.
- Bridge version, host version, and domain contract version are separate.
- Unknown optional fields are preserved or ignored according to the owning contract.
- Unknown required fields refuse.
- Unknown capabilities refuse.
- Deprecation requires owner record, migration path, and supersession evidence.
- Migration responsibility belongs to the owner of the semantic surface being migrated.
- No silent migration.
- No compatibility by filename coincidence.

AIDE and Dominium compatibility records must remain separate unless a future accepted bridge contract creates a versioned translation.
