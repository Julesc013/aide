# Persistence Flow

The fixture flow is:

```text
accepted local trust records
-> AuthorizationEvaluation
-> local Service trust events and grant consumption
-> accepted LocalProcessExecutionHost fixture run
-> WorkUnit object
-> WorkerRun object
-> ExecutionHostOutcome object
-> EvidencePacket object
-> EventRecord object
-> durable_worker_run.* local Service events
```

The committed source reports are scrubbed summaries. The local Service database
and content-addressed payload store are temporary by default and are not
committed.
