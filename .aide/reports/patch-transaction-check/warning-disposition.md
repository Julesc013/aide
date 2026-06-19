# Warning Disposition

The two path-scope findings are material failures, not warnings.

The following inherited or intentionally deferred boundaries remain warnings
only:

- minimal JSON Schema subset rather than full Draft validation;
- no general diff parser;
- no artifact resolver;
- no VCS reachability, branch existence, target existence, base ancestry, or
  clean-merge check;
- no policy evaluation;
- no approval engine;
- no apply engine;
- no rollback execution;
- no event store or replay;
- no conformance runner;
- no automatic observation collection;
- no profile activation;
- no adapter admission or trust;
- no runtime, worker execution, Test Broker, scheduler, leases, supervisor,
  Service, Commander, or Workbench.

These warnings do not by themselves block the schema-only slice. Acceptance is
blocked by the material path-scope defects.
