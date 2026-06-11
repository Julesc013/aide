# Future Work

Recommended next tasks, in order:

1. `AIDE-CHECK-CONTRACT-ENVELOPE-01`: independently review helper behavior,
   projections, validation, compatibility, report truth, tests, and
   no-overclaiming.
2. `AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01`: extract a minimal EvidencePacket
   shape after the envelope is checked.
3. `AIDE-BUILD-WORKUNIT-QUEUE-V1-01`: define the first minimal queue WorkUnit
   object after envelope and evidence shapes are accepted.
4. `AIDE-BUILD-WORKUNIT-CLI-01`: build the CLI after the queue object is
   stable.
5. `AIDE-BUILD-TEST-BROKER-01`: add asynchronous test broker primitives after
   WorkUnit primitives exist.
