# Prompt: AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01

Create and process a bounded, check-only queue WorkUnit that independently
reviews `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`.

This is not an implementation or repair task.

Check that the ConformanceResult slice:

- records observations against one exact ConformanceProfile version;
- is projected from existing committed evidence;
- binds to the exact profile ref, version, digest, and subject;
- represents every projected case result truthfully;
- computes aggregation according to the profile;
- separates record validity, record completeness, profile satisfaction,
  admission, subject admission, and trust;
- performs no execution, collection, admission, mutation, or runtime behavior.

Stop at `needs_review`.

If the check passes, recommend:

```text
AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01
```

If the check fails materially, recommend:

```text
AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
```

Do not repair the build implementation in this task.
