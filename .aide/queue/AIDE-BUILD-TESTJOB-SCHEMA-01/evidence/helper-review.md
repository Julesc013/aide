# Helper Review

Status: PASS.

`core/protocol/test_job.py` implements deterministic local helper behavior:

- loads the TestJob schema
- validates helper/schema alignment
- builds metadata-only TestJob records
- validates TestJob records
- tolerates unknown optional fields
- fails closed on unknown required capabilities
- projects accepted artifacts into additive TestJob JSON files
- writes status, projection, validation, future-work, and unfinished-work reports
- preserves explicit non-capabilities

The helper records runtime flags as false for Test Broker runtime, async execution, submission, run, retry runtime, summarize runtime, scheduler, leases, supervisor, worker execution, WorkUnit claim/run/finish/repair, Service, Commander, and provider adapters.
