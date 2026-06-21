# Digest Integrity Review

```json
{
  "mutations": [
    {
      "name": "validation_summary.validated",
      "observed_codes": [
        "digest.bundle_self"
      ],
      "result": "PASS"
    },
    {
      "name": "validation_summary.error_count",
      "observed_codes": [
        "digest.bundle_self"
      ],
      "result": "PASS"
    },
    {
      "name": "status.network_call_performed",
      "observed_codes": [
        "digest.bundle_self",
        "status.false_boundary"
      ],
      "result": "PASS"
    },
    {
      "name": "manifest.record_count",
      "observed_codes": [
        "digest.bundle_self",
        "record_count"
      ],
      "result": "PASS"
    },
    {
      "name": "omission_summary.reason",
      "observed_codes": [
        "digest.bundle_self"
      ],
      "result": "PASS"
    },
    {
      "name": "authority_classification.conflict_policy",
      "observed_codes": [
        "digest.bundle_self"
      ],
      "result": "PASS"
    },
    {
      "name": "registry_projection_summary.diagnostics.projected_count",
      "observed_codes": [
        "digest.bundle_self"
      ],
      "result": "PASS"
    }
  ],
  "result": "PASS"
}
```
