# Schema / Helper Alignment Review

Result: PASS

Direct in-memory and temp checks verified:

- valid envelope passes helper and schema validation
- missing `apiVersion`, `kind`, `metadata`, `spec`, and `status` are rejected
  by helper and schema validation
- wrong-type `metadata`, `spec`, and `status` are rejected by helper and schema
  validation
- unknown optional fields are tolerated
- unknown required capability fails closed
- unsupported broad capability label is rejected
- malformed schema copy missing required `status` fails alignment
- valid lifecycle run and verify projections pass helper and schema validation
- malformed projection fails helper and schema validation
- projection functions do not mutate source report dictionaries

Non-blocking note: compatibility SemVer semantics remain helper-enforced rather
than fully represented in JSON Schema; the report correctly states the schema
validator is a minimal subset.
