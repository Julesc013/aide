# WorkerRun Future Work

## Recommended Order

1. AIDE-CHECK-WORKER-RUN-SCHEMA-01: independent review of WorkerRun schema, helper validation, projections, compatibility, tests, no destructive migration, no overclaiming, and forbidden-operation preservation.
2. AIDE-BUILD-WORKER-RUN-HARDEN-01: harden only if the check finds validation, projection, or schema gaps.
3. AIDE-ACCEPT-WORKER-RUN-SCHEMA-01: accept WorkerRun only after check and any required hardening.
4. AIDE-BUILD-TESTJOB-SCHEMA-01: define TestJob schema before Test Broker.
5. AIDE-BUILD-WORKUNIT-CLAIM-LEASE-SCHEMA-01: define claim and lease schema before implementing claim.
6. AIDE-BUILD-WORKUNIT-CLAIM-CLI-01: add claim only after WorkerRun and lease shape are accepted.
