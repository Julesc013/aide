# Helper Review

Reviewed `core/protocol/conformance_result.py`.

Status:

```text
FAILED_VALIDATION
```

Most helper behavior is coherent:

- builds one evidence-projected result;
- records one case result per profile case;
- validates result, case, aggregation, and no-admission boundaries;
- writes deterministic reports;
- exposes status/project/validate behavior through the CLI.

Material defect:

```text
load_accepted_conformance_profile appends a lifecycle warning to an in-memory
profile copy before profile_digest is computed.
```

The validator recomputes the same mutated-view digest, so the helper reports
`profile_digest_matches: true` while an independent digest over the raw accepted
profile report does not match.

No helper repair was performed.
