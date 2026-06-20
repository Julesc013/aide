# Warning Disposition

Result classification is `PASS_WITH_WARNINGS`.

Warnings are non-blocking because the contract fails closed and does not claim
runtime behavior:

- A2A agent-card contract is projection-only.
- No live endpoint or registration exists.
- Full external A2A schema validation remains future work.
- Skills are future read-only discovery candidates only.
- Authentication, authorization, PolicyDecision, CapabilityGrant, credential
  handling, delegation, and worker execution remain absent.
- Inherited Interop Exports preview-only limitations and report/OKF/Reconciler
  warning debt remain unresolved.
