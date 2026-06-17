# OKF / ReferenceID / EventRecord Integration Review

Finding: pass with warnings.

Confirmed:

- Capability refs use accepted `aide://capability/<id>` syntax.
- Source refs use queue-task style refs where practical.
- Report refs use `aide://report/...` refs.
- Evidence refs use `aide://evidence/...` refs.
- Event refs exist for all projected capabilities.
- OKF refs are present where corresponding OKF capability pages exist.
- `reference-id validate` returned `PASS_WITH_WARNINGS`.
- `event-record validate` returned `PASS_WITH_WARNINGS`.
- `okf validate` and `okf lint` returned `PASS_WITH_WARNINGS`.
- CapabilityManifest does not create a new reference grammar.
- CapabilityManifest does not update OKF pages.
- CapabilityManifest does not emit runtime events.

Warning:

- Existing stale OKF/context drift remains warning-class and unresolved.
