# WorkUnit Queue Future Work

## Recommended Order

1. AIDE-CHECK-WORKUNIT-QUEUE-V1-01: independent review of WorkUnit queue schema, projections, compatibility, tests, and no-overclaiming.
2. AIDE-HARDEN-WORKUNIT-QUEUE-V1-01: harden only if the check finds validation, projection, or schema gaps.
3. AIDE-ACCEPT-WORKUNIT-QUEUE-V1-01: accept the minimal WorkUnit queue object only after check and any required hardening.
4. AIDE-BUILD-WORKUNIT-CLI-01: add WorkUnit create/list/claim/block/finish/repair only after queue object acceptance.
5. AIDE-BUILD-TESTJOB-SCHEMA-01: define TestJob after WorkUnit queue shape is accepted.
6. AIDE-BUILD-TEST-BROKER-01: build long-running test broker after WorkUnit and TestJob contracts exist.
