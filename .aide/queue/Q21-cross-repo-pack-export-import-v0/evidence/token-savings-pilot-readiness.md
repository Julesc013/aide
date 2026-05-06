# Token Savings Pilot Readiness

## Why Q21 Matters

Q21 makes the token-survival foundation portable enough to test in real target
repositories. Without this pack boundary, future agents would either copy too
much AIDE-specific state or rebuild AIDE Lite from long chat history.

The pack directly supports token savings by making these target-local workflows
available:

- compact task packets
- repo snapshots, maps, test maps, and context indexes
- verifier reports
- compact review packets
- token estimates and metadata-only ledger reports
- golden-task substrate gates
- advisory outcome and route reports
- cache/local-state boundary checks

## What Q22 Must Measure

The Eureka pilot must measure:

- whether imported AIDE Lite can generate Eureka-specific snapshot/index/pack
- compact packet size compared to a manual context dump or existing prompt
- verifier and golden-task status after target initialization
- whether target-specific memory can stay concise and accurate
- whether any source AIDE identity or generated state leaks into Eureka
- whether the workflow reduces prompt size without weakening review gates

## Quality Caveat

Fixture import proves the copy boundary and command smoke, not product value in
Eureka or Dominium. Token savings remain invalid if quality evidence, verifier
output, golden tasks, provenance, or review gates are weakened.

## Next Phase

Recommended next queue item:

```text
Q22 Eureka Import Pilot
```

Q22 should import the pack into Eureka, generate target-local context and task
packets, run validation, and compare prompt size and quality signals against a
manual baseline.
