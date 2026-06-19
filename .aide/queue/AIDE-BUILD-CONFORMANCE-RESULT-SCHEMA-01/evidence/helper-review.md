# Helper Review

Reviewed `core/protocol/conformance_result.py`.

The helper:

- loads the accepted ConformanceProfile candidate;
- computes a stable digest from the bound profile;
- builds one deterministic evidence-projected result;
- projects one case result per accepted profile case;
- aggregates required, optional, and advisory outcomes;
- validates profile binding, case-result semantics, aggregation consistency, and
  boundary flags;
- writes deterministic JSON and Markdown reports;
- records future work and explicit non-capabilities.

The helper does not run subprocesses, execute conformance cases, collect live
results, admit subjects, grant trust, call providers, mutate target repos, or
perform runtime behavior.
