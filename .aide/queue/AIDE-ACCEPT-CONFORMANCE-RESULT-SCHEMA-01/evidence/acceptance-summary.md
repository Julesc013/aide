# Acceptance Summary

Result:

```text
ACCEPTED_WITH_WARNINGS
```

Accepted capability:

```text
minimal_conformance_result_schema
```

Accepted scope:

- one evidence-projected ConformanceResult record;
- result, case-result, aggregation, profile-binding, digest-binding, validation,
  status, and index reports;
- `conformance-result status/project/validate` CLI dispatch;
- explicit non-capability preservation.

The accepted result ref is:

```text
aide://conformance-result/minimal_capability_manifest-v1.0.0-evidence-projection-01
```

The result binds to:

```text
aide://conformance-profile/minimal_capability_manifest-v1.0.0
```

The accepted profile digest is:

```text
sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70
```

The historical failed check remains retained as evidence, and the repair plus
repair-check chain corrected the digest authority defect.

Recommended next task:

```text
AIDE-OPERATIONAL-HEALTH-PAUSE-01
```
