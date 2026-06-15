# Schema Review

Result: PASS_WITH_WARNINGS.

Verified:

- `.aide/protocol/aide-test-job.schema.json` exists and parses as JSON.
- `kind` is constrained to `TestJob`.
- Required top-level fields are `apiVersion`, `kind`, `metadata`, `spec`, and `status`.
- Compatibility metadata includes schema/protocol/min reader/min writer/feature flag fields and `requiredCapabilities`.
- `spec` includes command, environment, framework, timeout, artifacts, logs, evidence refs, explicit non-capabilities, failure summary, retry, and source metadata.
- `status` includes phase, result, start/end, exit code, duration, validation state, errors, and warnings.

Warning:

- Full JSON Schema Draft 2020-12 execution remains deferred; the slice uses the accepted minimal local subset validator.
