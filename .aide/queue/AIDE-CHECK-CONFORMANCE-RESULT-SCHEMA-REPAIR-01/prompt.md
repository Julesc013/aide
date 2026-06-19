# Prompt: AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01

Create and process a bounded, check-only queue WorkUnit that independently
reviews `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`.

This is not an implementation, repair, or acceptance task.

Check that the ConformanceResult repair:

- preserves the historical failed `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01`
  evidence;
- binds the result to the exact profile ref
  `aide://conformance-profile/minimal_capability_manifest-v1.0.0`;
- computes the recorded profile digest using `sha256-canonical-json-v1` over the
  pristine accepted profile payload;
- fails validation for an incorrect digest;
- does not allow lifecycle-warning mutation on a copy to become digest
  authority;
- does not mutate the source profile during projection or validation;
- preserves result, case, aggregation, evidence-projection, execution,
  admission, subject admission, and trust boundaries.

Stop at `needs_review`.

If the recheck passes, recommend:

```text
AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01
```

If the digest remains incorrect, recommend:

```text
AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-02
```

Do not repair implementation artifacts in this task.
