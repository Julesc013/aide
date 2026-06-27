# Accepted MigrationRecord v0 Contract

MigrationRecord v0 is accepted as no-apply migration decision metadata.

Accepted behavior:

- bind source object ref and digest
- record source and target schema versions
- record migration kind and plan ref
- record field mapping summary
- record unknown-field disposition
- require manual review for ambiguous migrations
- require rollback requirements for destructive migrations
- preserve evidence refs and explicit non-capabilities
- fail closed on source latest output misuse and source output as target truth
