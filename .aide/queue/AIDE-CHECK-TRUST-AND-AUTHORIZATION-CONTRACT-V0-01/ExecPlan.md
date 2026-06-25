# AIDE-CHECK-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01 ExecPlan

## Objective

Independently check the projection-only trust and authorization contract build
without modifying production code, schemas, build reports, or source task
evidence.

## Scope

Allowed writes are limited to this check task packet, the check report directory,
`.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Plan

1. Confirm repository and source-task baseline.
2. Inspect committed trust schemas, projection files, reports, source evidence,
   and focused tests.
3. Run an independent data-only harness that does not import
   `core.protocol.trust_authorization`.
4. Run focused and broad validation commands.
5. Write check reports and route to the exact next task.
6. Stop at `needs_review`.

## Validation Intent

Validate stable AIDE refs, no embedded credentials or secrets, exact-digest
admission, declaration/conformance/admission separation, policy/grant
separation, scope and delegation bounds, revocation and expiry fail-closed
coverage, use-budget consistency, runtime-vs-transaction approval separation,
unknown required feature fail-closed behavior, schema/projection alignment,
deterministic serialization, complete refusal-code coverage, and truthful
projection-only non-capability claims.

## Result

PASS_WITH_WARNINGS. No material findings were found. The next task is
`AIDE-ACCEPT-TRUST-AND-AUTHORIZATION-CONTRACT-V0-01`.
