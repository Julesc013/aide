# Future Work

Recommended order:

1. `AIDE-CHECK-EVIDENCE-PACKET-SCHEMA-01`: independent review of helper behavior,
   schema/helper alignment, projection outputs, source traceability,
   compatibility, tests, no destructive migration, no overclaiming, and
   forbidden-operation preservation.
2. `AIDE-BUILD-EVIDENCE-PACKET-HARDEN-01`: harden only if the check finds
   validation, projection, or schema gaps.
3. `AIDE-ACCEPT-EVIDENCE-PACKET-SCHEMA-01`: acceptance review after check and
   any required hardening.
4. `AIDE-BUILD-WORKUNIT-QUEUE-V1-01`: define minimal queue WorkUnit object after
   envelope and evidence shapes are accepted.
5. `AIDE-BUILD-WORKUNIT-CLI-01`: add WorkUnit CLI only after queue object is
   stable.

Do not mark these future tasks complete in this turn.
