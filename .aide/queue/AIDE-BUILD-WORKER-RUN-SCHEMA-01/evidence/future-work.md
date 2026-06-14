# Future Work

Recommended next task:

```text
AIDE-CHECK-WORKER-RUN-SCHEMA-01
```

Later, only after independent check and acceptance:

- Harden WorkerRun if CHECK finds defects.
- Accept WorkerRun after check/hardening.
- Build TestJob schema before Test Broker.
- Define claim and lease schema before implementing WorkUnit claim.
- Add WorkUnit claim/run behavior only after WorkerRun, lease shape, and TestJob/Test Broker boundaries are accepted.
