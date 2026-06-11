# Contract Envelope Future Work

## Recommended Order

1. AIDE-CHECK-CONTRACT-ENVELOPE-HARDEN-01: independent review of schema runtime loading, helper/schema alignment, compatibility, tests, and no-overclaiming.
2. AIDE-ACCEPT-CONTRACT-ENVELOPE-01: accept the envelope only after the hardening check passes.
3. AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01: extract minimal EvidencePacket shape after the envelope is accepted.
4. AIDE-BUILD-WORKUNIT-QUEUE-V1-01: define minimal queue WorkUnit object after envelope and evidence shapes are accepted.
