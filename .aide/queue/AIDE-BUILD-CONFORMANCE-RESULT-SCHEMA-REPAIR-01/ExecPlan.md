# AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01 ExecPlan

## Objective

Repair the ConformanceResult profile digest binding defect found by
`AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01`.

## Scope

- Compute profile digests from the pristine accepted ConformanceProfile payload.
- Use the explicit `sha256-canonical-json-v1` algorithm.
- Prevent validation-warning annotation from becoming digest authority.
- Add regression tests with independent `hashlib` recomputation.
- Regenerate affected ConformanceResult reports.
- Write repair-specific reports, evidence, and next-task prompt.

## Dependencies

- Failed check: `AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01`.
- Original build: `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`.
- Accepted profile: `aide://conformance-profile/minimal_capability_manifest-v1.0.0`.

## Milestones

- Reproduce the digest mismatch from live evidence.
- Identify root cause in profile loading and digest validation.
- Repair digest source and ordering.
- Add regression tests.
- Regenerate reports.
- Validate and stop at `needs_review`.

## Verification Intent

Run Python compile checks, focused ConformanceResult tests, independent digest
recomputation, repeated projection determinism checks, ConformanceResult
status/project/validate, JSON report parsing, predecessor validators, task
inspect/evidence checks, broad AIDE validation, Git diff checks, a secret-like
scan, and commit policy validation.

## Exit Criteria

The task stops at `needs_review` with `PASS_WITH_WARNINGS`, corrected result
digest equals independent pristine-profile digest, source profile remains
unchanged, case and aggregation semantics remain unchanged, no execution or
admission is added, and the next task is
`AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01`.

## Non-Capabilities

This repair does not accept ConformanceResult, execute cases, implement a
runner, collect live observations, activate a profile, admit a subject, grant
trust, implement adapters, implement PatchTransaction, implement runtime, mutate
target repositories, call providers/models/network/Gateway, publish releases, or
promote branches.
