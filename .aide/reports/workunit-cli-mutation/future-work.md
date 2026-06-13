# WorkUnit CLI Mutation Future Work

## Recommended Order

1. AIDE-CHECK-WORKUNIT-CLI-MUTATION-01: independent review of create/block/evidence-add behavior, dry-run/apply semantics, path safety, mutation locality, compatibility, no runtime, no overclaiming, and tests.
2. AIDE-BUILD-WORKUNIT-CLI-MUTATION-HARDEN-01: harden only if the check finds command, path, report, compatibility, or mutation-safety gaps.
3. AIDE-ACCEPT-WORKUNIT-CLI-MUTATION-01: accept the metadata mutation CLI after check and any required hardening.
4. AIDE-BUILD-WORKER-RUN-SCHEMA-01: define WorkerRun before claim/run semantics or agent adapters.
5. AIDE-BUILD-TESTJOB-SCHEMA-01: define TestJob before Test Broker.
6. AIDE-BUILD-WORKUNIT-CLAIM-LEASE-SCHEMA-01: define claim and lease schema before implementing claim.
