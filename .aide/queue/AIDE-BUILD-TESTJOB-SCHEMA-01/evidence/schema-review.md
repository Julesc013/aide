# Schema Review

Status: PASS_WITH_WARNINGS.

`.aide/protocol/aide-test-job.schema.json` exists and parses as JSON. It declares `kind: TestJob`, uses `apiVersion`, `kind`, `metadata`, `spec`, and `status`, and keeps `additionalProperties: true` for additive compatibility.

The schema includes compatibility metadata, command/cwd/env policy metadata, environment metadata, framework metadata, timeout metadata, artifact/log references, evidence packet references, failure-summary placeholders, retry/flake placeholders, and explicit non-capabilities.

The schema requires `status.phase`, `status.result`, `status.validated`, `status.validation_errors`, and `status.validation_warnings`, with nullable start/end/exit/duration metadata.

Warning: validation follows the accepted local minimal JSON Schema subset; full Draft 2020-12 validation remains future conformance work.
