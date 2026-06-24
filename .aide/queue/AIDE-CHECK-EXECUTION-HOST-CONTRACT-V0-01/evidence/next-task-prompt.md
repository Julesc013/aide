# Next Task Prompt

```text
Create and process
AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01.

Review AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01 and
AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01.

Accept only:

execution_host_contract_v0

as a projection-only ExecutionHost contract v0 defining descriptor, run
binding, event, artifact, approval, usage, operation vocabulary, false-boundary
fields, and explicit non-capabilities.

Do not accept or implement:

- live ExecutionHost;
- LocalProcessExecutionHost;
- RemoteExecutionHost;
- worker execution;
- worker harness;
- scheduler or supervisor;
- Service/runtime behavior;
- Workbench behavior;
- provider/model/network calls;
- PreviewSession;
- DevelopmentTransaction;
- PatchTransaction apply;
- repository mutation;
- branch/worktree mutation;
- GitHub mutation;
- release or promotion.

If accepted, recommend exactly:

AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-01.
```
