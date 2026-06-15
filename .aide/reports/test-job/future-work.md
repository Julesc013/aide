# TestJob Future Work

## Recommended Order

1. AIDE-CHECK-TESTJOB-SCHEMA-01: independent review of TestJob schema, helper validation, projections, compatibility, tests, no destructive migration, no overclaiming, and forbidden-operation preservation.
2. AIDE-ACCEPT-TESTJOB-SCHEMA-01: accept TestJob only after check and any required hardening.
3. AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01: define patch transaction protocol after TestJob acceptance.
4. AIDE-BUILD-BLOCKER-REPAIR-SCHEMAS-01: define blocker and repair objects before repair loops.
5. AIDE-BUILD-CAPABILITY-MANIFEST-01: declare capabilities before runtime/service surfaces.
6. AIDE-BUILD-ADAPTER-MANIFEST-01: declare adapter conformance before provider adapters.
7. AIDE-BUILD-EVENT-RECORD-SCHEMA-01: define event records before scheduler/runtime implementation.
8. AIDE-BUILD-TEST-BROKER-RUNTIME-01: future only after TestJob protocol acceptance.
