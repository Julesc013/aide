# Prompt: AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01

Accept or reject only the checked `minimal_event_record_schema` capability after reviewing:

- `AIDE-ACCEPT-REFERENCE-ID-SCHEME-01`
- `AIDE-BUILD-EVENT-RECORD-SCHEMA-01`
- `AIDE-CHECK-EVENT-RECORD-SCHEMA-01`

This is a check-only acceptance gate. It must not repair EventRecord, implement OKF, or authorize runtime work.

If accepted, recommend exactly:

```text
AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01
```
