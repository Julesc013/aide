# Lifecycle Fixture Runner Future Work

## Recommended Order

1. AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CHECK-01: independently review temp-only mutation, path jail, canonical fixture no-mutation, reports, rollback-compatible record, tests, and capability labels.
2. AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01: harden malformed marker, duplicate marker, nested marker, and edge-case failure reporting.
3. AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CONFORMANCE-01: add conformance fixtures for supported and unsupported scenarios and modes.
4. AIDE-BUILD-CONTRACT-ENVELOPE-01: introduce a minimal envelope only after this slice is reviewed.
5. AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01: formalize evidence packets from proven fields.
6. AIDE-BUILD-WORKUNIT-CLI-01: begin simple WorkUnit CLI after lifecycle review.
7. AIDE-BUILD-TEST-BROKER-01: add async test broker after WorkUnit primitives exist.
8. AIDE-BUILD-PROMOTION-POLICY-01: add policy-driven promotion later without hardcoding dev/main.
9. AIDE-BUILD-CODEX-ADAPTER-01: add Codex only after WorkUnit/Evidence/TestJob contracts exist.
10. AIDE-BUILD-COMMANDER-READONLY-01: add Commander read-only cockpit after core CLI/service substrate exists.
