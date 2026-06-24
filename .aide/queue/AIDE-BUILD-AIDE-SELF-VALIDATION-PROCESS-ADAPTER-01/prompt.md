# AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01

Create and process `AIDE-BUILD-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01`.

Repo truth outranks this prompt. Use `.aide/queue/index.yaml`, the registered
process provider repair check evidence, `PLANS.md`, `IMPLEMENT.md`, and live
repository state as operational truth.

Goal: prove reuse of the proposed generic `RegisteredProcessExecutionProvider
v0` by invoking AIDE itself through one thin declarative adapter.

Authorized process shape:

```text
<python> .aide/scripts/aide_lite.py validate
```

Requirements:

- do not change generic provider core;
- use `subprocess` through the registered-process provider with `shell=False`;
- invoke exactly one successful live AIDE Lite validate process;
- use focused fake-runner unit tests for other scenarios;
- keep unsupported capabilities and invalid requests at zero launches;
- preserve the shared `ProcessExecutionReceipt` and `CapabilityOutcome` model;
- prove before/after AIDE state is unchanged within declared probe coverage;
- scrub absolute local paths and secret-like values from committed reports;
- write complete queue evidence and reports;
- stop at `needs_review`;
- recommend exactly `AIDE-CHECK-AIDE-SELF-VALIDATION-PROCESS-ADAPTER-01`.

Forbidden:

- accepting the registered-process provider;
- changing `core/execution/registered_process.py`;
- changing neutral process invocation or receipt protocol files;
- generic arbitrary command dispatch;
- Dominium or Eureka adapter changes;
- provider/model/network calls;
- worker execution;
- Service, Workbench, preview, apply, rollback, PatchTransaction apply;
- source or target repository mutation;
- branch/worktree, GitHub, release, or promotion behavior.
