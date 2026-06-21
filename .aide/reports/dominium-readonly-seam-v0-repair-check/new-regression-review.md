# New Regression Review

```json
{
  "direct_injections": [
    {
      "expected_code": "revision.binding",
      "name": "mixed_record_revision",
      "observed_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "revision.binding"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "digest.snapshot",
      "name": "snapshot_digest",
      "observed_codes": [
        "digest.bundle_self",
        "digest.snapshot"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "cardinality.singleton",
      "name": "second_host_capability_set",
      "observed_codes": [
        "capability.forbidden_set",
        "capability.implemented_set",
        "cardinality.singleton",
        "digest.bundle_self",
        "digest.projection_index",
        "identity.duplicate",
        "record_count"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "reference.closure",
      "name": "dangling_artifact",
      "observed_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "reference.closure"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "ownership.semantic",
      "name": "wrong_owner",
      "observed_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "ownership.semantic"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "capability.mutation",
      "name": "forbidden_capability",
      "observed_codes": [
        "capability.implemented_set",
        "capability.mutation",
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "event.sequence",
      "name": "duplicate_event_sequence",
      "observed_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "event.sequence"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "diagnostic.registry",
      "name": "bad_diagnostic_severity",
      "observed_codes": [
        "diagnostic.registry",
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "refusal.registry",
      "name": "invented_refusal",
      "observed_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "refusal.registry"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "spec.required",
      "name": "missing_host_id",
      "observed_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "spec.required"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "event.causation",
      "name": "wrong_causation",
      "observed_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "event.causation"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "diagnostic.registry",
      "name": "wrong_diagnostic_summary",
      "observed_codes": [
        "diagnostic.registry",
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "refusal.registry",
      "name": "wrong_refusal_recovery",
      "observed_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "refusal.registry"
      ],
      "result": "PASS"
    },
    {
      "expected_code": "spec.type",
      "name": "wrong_host_id_type",
      "observed_codes": [
        "digest.bundle_self",
        "digest.projection_index",
        "digest.record",
        "spec.type"
      ],
      "result": "PASS"
    }
  ],
  "material_gaps": [
    "allowed_operation_count missing",
    "conformance results lack required independent assertion fields",
    "cross-process determinism failed",
    "diagnostic projection disclosure is incomplete",
    "instrumentation coverage missing",
    "ledger does not describe every required operation family",
    "one or more replayable negative fixtures failed independent replay",
    "public schema does not constrain kind-specific spec fields",
    "public schema does not constrain status facts",
    "refusal projection disclosure is incomplete"
  ]
}
```
