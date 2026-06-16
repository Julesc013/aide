# Acceptance Summary

Result: ACCEPTED_WITH_WARNINGS.

Accepted capability:

```text
minimal_reference_id_scheme
```

Accepted behavior:

- `aide://<kind>/<id>` stable identity syntax.
- ReferenceID schema/helper/projection/validation.
- `reference-id status/project/validate` CLI dispatch.
- Deterministic reference-map reports.
- File paths as locators, not identity.
- Optional SHA-256 locator metadata.
- Unknown required ref kinds fail closed.
- Unknown optional ref kinds warn/tolerate where intended.
- Predecessor compatibility with ContractEnvelope, EvidencePacket, WorkUnit, WorkerRun, and TestJob.

Source evidence:

- `AIDE-BUILD-REFERENCE-ID-SCHEME-01`: `PASS_WITH_WARNINGS`.
- `AIDE-CHECK-REFERENCE-ID-SCHEME-01`: `PASS_WITH_WARNINGS`.
- Build evidence missing: 0.
- Check evidence missing: 0.
- Projected refs: 25.
- Required locators missing: 0.
- Required locators without SHA-256: 0.

Warnings are accepted because they are truthful, non-blocking, and do not expand the accepted capability.

Recommended next task:

```text
AIDE-BUILD-EVENT-RECORD-SCHEMA-01
```

This acceptance does not authorize EventRecord implementation by itself. It only records the next queued build prompt to create.
