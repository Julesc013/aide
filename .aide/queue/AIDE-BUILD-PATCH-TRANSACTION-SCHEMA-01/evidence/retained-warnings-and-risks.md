# Retained Warnings And Risks

Result classification: `PASS_WITH_WARNINGS`.

Warnings retained from the operational-health pause:

- report volume and report ambiguity;
- generated-output unknown provenance;
- one stale-context OKF finding;
- four Reconciler warning findings;
- queue review-gate versus capability-state readability debt.

PatchTransaction-specific warnings:

- no apply engine exists;
- policy evaluation is not implemented;
- approval is not implemented or granted;
- artifact resolution and VCS reachability are not implemented;
- admission and trust are not implemented;
- runtime behavior is not implemented.

None of these warnings blocks a schema-only PatchTransaction check. They would
block any claim of controlled apply, autonomous mutation, admission, trust, or
runtime execution.
