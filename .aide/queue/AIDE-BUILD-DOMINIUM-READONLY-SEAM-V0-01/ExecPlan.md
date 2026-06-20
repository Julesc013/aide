# AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01 ExecPlan

## Objective

Build the complete offline, deterministic, read-only AIDE-Dominium seam v0 as one vertical slice.

## Scope

- Create public v0 seam contracts and a cohesive `core/interop/dominium/` implementation package.
- Read an already-present Dominium checkout or Git object without fetch, pull, checkout, command invocation, or file mutation.
- Project HostManifest, HostCapabilitySet, WorkspaceDescriptor, ContextDescriptor, ArtifactReference, DiagnosticProjection, RefusalProjection, EvidenceReferenceSet, EventEnvelope, DominiumBridgeManifest, and SeamBundle outputs.
- Add CLI commands for `dominium-seam status`, `snapshot`, `project`, `validate`, `diff`, and `demo`; unsupported mutation/runtime verbs fail closed.
- Write positive and adversarial fixtures, focused tests, deterministic reports, and consolidated evidence.

## Plan

1. Verify predecessor acceptance, clean AIDE state, available read-only Dominium input, and absence of superseding seam tasks.
2. Materialize queue packet and allowed-path scope.
3. Implement schema bundle and shared Python package.
4. Add CLI dispatch in `aide_lite.py`.
5. Add positive/adversarial fixtures and focused tests.
6. Run projection, validation, repeated deterministic projection comparison, and offline demo.
7. Record reports and task-local evidence.
8. Run focused tests, broad validation, secret scan, diff checks, and commit-policy validation.
9. Stop at `needs_review` and recommend `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01`.

## Constraints

- Dominium is read-only input.
- No fetch, pull, checkout, branch/worktree automation, remote-ref mutation, Dominium command invocation, provider/model/network call, worker execution, service, transport, preview/apply/rollback, PatchTransaction apply, target mutation, GitHub mutation, release, or promotion.
- SeamBundle is generated projection evidence, not canonical product truth.

## Validation Intent

- Python compilation.
- Focused seam unittest suite.
- Positive and negative fixture validation.
- Full offline demo.
- Repeated projection byte equality.
- Source digest recomputation and Dominium immutability checks.
- Unsupported CLI operation probes.
- `git diff --check`, `git diff --cached --check`, broad `aide_lite.py validate`, task inspect/evidence, and commit check.
