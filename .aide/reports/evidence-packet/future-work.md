# EvidencePacket Future Work

## Recommended Order

1. AIDE-CHECK-EVIDENCE-PACKET-SCHEMA-01: independent review of EvidencePacket schema, helper validation, projections, source traceability, compatibility, tests, and no-overclaiming.
2. AIDE-BUILD-EVIDENCE-PACKET-HARDEN-01: harden only if the check finds validation, projection, or schema gaps.
3. AIDE-ACCEPT-EVIDENCE-PACKET-SCHEMA-01: accept the EvidencePacket schema only after check and any required hardening.
4. AIDE-BUILD-WORKUNIT-QUEUE-V1-01: define minimal queue WorkUnit object after envelope and evidence shapes are accepted.
5. AIDE-BUILD-WORKUNIT-CLI-01: add WorkUnit CLI only after queue object is stable.
