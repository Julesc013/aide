# Accepted Boundary

Accepted:

- fixture-backed LocalProcessExecutionHost reference slice;
- exactly one allowlisted local reference worker launch through the accepted RegisteredProcessExecutionProvider v0;
- disposable workspace staging and containment checks;
- fail-closed raw NDJSON event stream parsing;
- verified content-addressed raw event and worker artifact evidence;
- WorkerRun lifecycle projection for supported terminal fixture states;
- deterministic report and projection generation for this fixture slice.

Not accepted:

- generic worker harness;
- autonomous AI worker;
- arbitrary command execution;
- remote ExecutionHost;
- Service/runtime behavior;
- Workbench/MCP behavior;
- provider/model/network calls;
- preview/apply/rollback;
- repository mutation;
- branch/worktree automation;
- GitHub mutation;
- release or promotion.
