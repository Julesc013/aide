# Schema / Helper Alignment Review

Result: PASS

Direct helper/schema checks verified:

- valid minimal envelope accepted by helper and schema
- missing `apiVersion`, `kind`, `metadata`, `spec`, and `status` rejected
- wrong type for `metadata`, `spec`, and `status` rejected
- unknown optional fields tolerated
- unknown required capability fails closed
- `fixture_temp_apply_only` accepted
- unsupported broad capability rejected
- malformed schema missing required declarations fails alignment
- valid lifecycle run projection passes helper and schema validation
- valid lifecycle verify projection passes helper and schema validation
- malformed projection fails validation
- projection functions do not mutate source report dictionaries

The acceptance run recorded 29 direct negative/alignment checks with zero
failures.
