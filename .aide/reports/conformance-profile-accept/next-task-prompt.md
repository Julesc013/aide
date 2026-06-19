# AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01
# Minimal Observed AIDE ConformanceResult Protocol Slice

Create and process `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`.

Use `.aide/queue/index.yaml` as canonical queue truth.

## Goal

Implement the first minimal, observed-result-only ConformanceResult protocol
slice against the accepted candidate profile:

```text
aide://conformance-profile/minimal_capability_manifest-v1.0.0
```

ConformanceResult records observations.

It does not execute checks. It does not admit a subject. It does not activate a
profile. It does not confer trust.

## Build Only

- ConformanceResult schema
- nested per-case observed result model
- deterministic helper/projection/validation
- one fixture/result projection derived from existing build/check/accept evidence
- result/index reports
- `conformance-result status/project/validate` CLI
- focused tests
- queue evidence

## Result References

The result must reference:

- exact profile ref
- exact profile version
- subject ref
- each observed case result
- evidence refs
- timestamps or source versions where deterministic
- warnings and limitations
- aggregation outcome

## Observed Outcomes

Required observed outcomes should distinguish:

- PASS
- PASS_WITH_WARNINGS
- FAIL
- ERROR
- SKIPPED
- UNAVAILABLE
- NOT_RUN

Aggregation must preserve profile law:

- all required cases must pass or pass with accepted warnings
- missing required case fails closed
- skipped required case fails closed
- unavailable required case fails closed
- optional failure remains warning-class
- advisory failure remains informational

## Do Not Implement

- a conformance runner
- command execution
- automatic result collection
- automatic admission
- policy approval
- profile activation
- adapter admission
- adapter execution
- capability execution
- PatchTransaction
- AdapterManifest
- ContextPack v2
- runtime
- Service
- Commander
- provider/model/network/Gateway/GitHub calls
- branch/worktree automation
- target apply
- rollback
- release or production readiness

Stop at `needs_review`.

Recommended next task:

```text
AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01
```
