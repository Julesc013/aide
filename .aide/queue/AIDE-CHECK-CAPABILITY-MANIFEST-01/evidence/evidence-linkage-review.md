# Evidence Linkage Review

Finding: pass with warnings.

Structured checks confirmed:

- Every projected capability has source refs.
- Every projected capability has evidence refs.
- Every projected capability has report refs.
- Every projected capability has an event ref.
- Referenced source, evidence, report, and OKF paths exist where paths are
  provided.
- Capability refs use `aide://capability/<id>` syntax.
- Evidence refs use `aide://evidence/...` syntax.
- Report refs use `aide://report/...` syntax.

Warning:

- Not every capability has an OKF page; missing OKF refs are expected where no
  corresponding OKF page exists and are not repaired by CapabilityManifest.
