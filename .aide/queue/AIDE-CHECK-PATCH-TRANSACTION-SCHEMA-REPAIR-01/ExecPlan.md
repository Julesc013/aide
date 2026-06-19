# AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01 ExecPlan

## Objective

Independently recheck the PatchTransaction path-scope repair without modifying
the PatchTransaction implementation, schema, tests, original failed-check
reports, repair reports, or already-blocked downstream task records.

## Scope

- Verify the original failed check remains preserved.
- Verify the repair rejects drive-prefixed path forms before ordinary
  repo-relative normalization.
- Verify duplicate-normalized path entries fail closed in `allowed_paths`,
  `forbidden_paths`, and `declared_changed_paths`.
- Verify duplicate diagnostics include both original inputs, the shared
  canonical value, and the affected path collection.
- Verify existing scope protections, no-apply status facts, CLI boundaries,
  deterministic projection, and source immutability.
- Classify downstream blocked tasks as historical blockers eligible for explicit
  resume after repair acceptance.

## Allowed Paths

- `.aide/queue/AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01/**`
- `.aide/reports/patch-transaction-repair-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

## Non-Goals

This check does not repair implementation, alter schema or tests, accept
PatchTransaction, apply patches, approve transactions, mutate repositories,
implement policy, rollback, admission, trust, AdapterManifest, ContextPack v2,
runtime, providers, hosts, VCS, Commander, Workbench, Service, release, or
promotion behavior.

## Dependencies

- `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01` exists at `needs_review` with result
  `PASS_WITH_WARNINGS`.
- `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01` exists at `needs_review` with result
  `FAILED_VALIDATION`.
- `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01` exists at `needs_review` with
  result `PASS_WITH_WARNINGS`.
- Hardening commit `fca99236c2f933660de29b657dc181f1174dd719` is live `HEAD`.

## Milestones

- Source chain reviewed.
- Independent drive-prefix and duplicate-normalization probes run.
- Diagnostic quality and scope regression behavior reviewed.
- CLI unsupported-operation probes run.
- Determinism and immutability checked in a temporary workspace.
- Downstream blocked records reviewed without mutation.
- Reports and task evidence written.
- Validation matrix run and evidence completed.

## Progress

- Live queue source chain satisfies the repair-check starting gate.
- Independent probes show all requested drive-prefix variants fail closed.
- Independent probes show duplicate-normalized path entries fail closed in all
  three relevant collections.
- Diagnostics identify both original values and the shared canonical path.
- The current strict allowed/forbidden overlap rule is preserved. Nested
  forbidden scope under an allowed scope remains invalid and is not changed by
  this check.
- Unsupported apply/approve/execute/rollback subcommands fail closed.
- Downstream blocked tasks remain historical records and require explicit resume
  tasks.

## Verification Intent

Run Git status and diff checks, Python compilation, focused PatchTransaction
unit tests, PatchTransaction status/project/validate, predecessor protocol
validators, repair and repair-check task inspect/evidence checks, broad AIDE
validation, JSON parsing, direct path probes, duplicate diagnostic assertions,
repeated projection comparison, source immutability comparison, original
failed-check preservation review, blocked downstream-record review,
unsupported subcommand probes, secret-like scan, and commit-policy validation.

## Exit Criteria

Stop at `needs_review` with `PASS_WITH_WARNINGS`; both original material path
defects are independently rechecked as fixed; diagnostics are sufficient; no
implementation or forbidden operation occurred; evidence is complete; and the
exact next task is `AIDE-RESUME-ACCEPT-PATCH-TRANSACTION-SCHEMA-01`.
