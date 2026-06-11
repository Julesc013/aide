# Future Work

1. `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CHECK-01`
   Independent review of temp-only mutation, path jail, canonical fixture no-mutation, reports, rollback-compatible record, tests, and capability labels.

2. `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01`
   Harden malformed marker detection, duplicate/nested marker failures, preimage mismatch failures, and clearer failure reports.

3. `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CONFORMANCE-01`
   Add conformance fixtures for supported and unsupported scenarios and modes.

4. `AIDE-BUILD-CONTRACT-ENVELOPE-01`
   Introduce minimal `apiVersion`/`kind`/`metadata`/`spec`/`status` envelopes after this runner is reviewed.

5. `AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01`
   Formalize EvidencePacket fields after this runner's evidence shape is reviewed.

6. `AIDE-BUILD-WORKUNIT-CLI-01`
   Begin simple WorkUnit CLI after lifecycle slice review.

7. `AIDE-BUILD-TEST-BROKER-01`
   Add async test broker after WorkUnit primitives exist.

8. `AIDE-BUILD-PROMOTION-POLICY-01`
   Add policy-driven branch/promotion behavior later; do not hardcode dev/main in this slice.

9. `AIDE-BUILD-CODEX-ADAPTER-01`
   Add Codex as a provider adapter only after WorkUnit/Evidence/TestJob contracts exist.

10. `AIDE-BUILD-COMMANDER-READONLY-01`
    Add Commander as a read-only cockpit after the core CLI/service substrate exists.
