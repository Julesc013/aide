# AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01

Create and process `AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01`.

Repo truth outranks this prompt. Use `.aide/queue/index.yaml` as canonical queue
truth and preserve the accepted RegisteredProcessExecutionProvider v0 and
ExecutionHost contract v0 boundaries.

Goal:

Build a bounded LocalProcessExecutionHost v0 reference implementation that starts
exactly one allowlisted local reference worker process and records typed
evidence without exposing arbitrary commands or broader runtime behavior.

Required proof chain:

```text
accepted ExecutionHost contract v0
accepted RegisteredProcessExecutionProvider v0
→ LocalProcessExecutionHost descriptor
→ exact allowlisted local reference worker argv
→ shell=False process launch
→ typed result or refusal
→ ProcessExecutionReceipt
→ ExecutionHost run binding/event/artifact/usage projections
→ EvidencePacket
→ EventRecord
→ deterministic read-only projection
```

Implementation requirements:

- use `RegisteredProcessExecutionProvider v0` without modifying provider core;
- use one committed local reference worker fixture;
- use subprocess through the provider with `shell=False`;
- launch exactly one process for the valid run;
- refuse unsupported capability, wrong revision, digest mismatch, malformed output,
  nonzero exit, timeout, schema mismatch, and unexpected mutation;
- preserve source state within declared probe coverage;
- scrub absolute local paths and secret-like values from committed evidence;
- add focused fake-runner tests;
- emit complete reports under `.aide/reports/local-process-execution-host/`;
- stop at `needs_review`.

Forbidden:

- arbitrary command execution;
- generic worker harness;
- autonomous AI worker;
- remote execution host;
- scheduler, supervisor, leases, durable Service/runtime;
- Workbench behavior;
- provider/model/network calls;
- PreviewSession, DevelopmentTransaction, PatchTransaction apply;
- source or target repository mutation;
- branch/worktree or GitHub mutation;
- release or promotion.

Recommend exactly:

```text
AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-01
```
