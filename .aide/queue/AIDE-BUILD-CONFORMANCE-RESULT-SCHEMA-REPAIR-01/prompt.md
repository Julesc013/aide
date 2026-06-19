# Prompt: AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01

Repair the material profile digest defect found by
`AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01`.

The ConformanceResult digest must bind to the pristine accepted
ConformanceProfile payload selected by exact profile ref:

```text
aide://conformance-profile/minimal_capability_manifest-v1.0.0
```

Use `sha256-canonical-json-v1`:

```python
json.dumps(profile, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
```

The repair must not change case outcomes, aggregate semantics, admission state,
trust state, accepted profile artifacts, accepted CapabilityManifest artifacts,
or historical failed-check evidence.

Stop at `needs_review` and recommend:

```text
AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
```
