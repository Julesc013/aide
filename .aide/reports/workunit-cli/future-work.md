# WorkUnit CLI Future Work

## Recommended Order

1. AIDE-CHECK-WORKUNIT-CLI-01: independent review of read-only WorkUnit CLI commands, path safety, compatibility, no destructive mutation, no overclaiming, and tests.
2. AIDE-BUILD-WORKUNIT-CLI-HARDEN-01: harden only if the check finds command, path, report, or compatibility gaps.
3. AIDE-ACCEPT-WORKUNIT-CLI-01: accept the read-only CLI after check and any required hardening.
4. AIDE-BUILD-WORKUNIT-CLI-MUTATION-01: add create/block-style mutation only after read-only CLI acceptance.
5. AIDE-BUILD-WORKER-RUN-SCHEMA-01: define WorkerRun before agent adapters.
6. AIDE-BUILD-TESTJOB-SCHEMA-01: define TestJob after the read-only WorkUnit CLI is accepted.
