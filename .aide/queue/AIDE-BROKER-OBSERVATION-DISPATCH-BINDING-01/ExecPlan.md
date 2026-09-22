# ExecPlan: Broker Observation-To-Dispatch Binding

## Objective

Bind every registered provider mutation child to the exact durable observation
that selected its stage, without widening transport, credential, host, or target
authority.

## Scope

- Adopt only the stage-effect and observed-closeout clauses derived from
  `UR-INT-06` and `UR-INT-07`.
- Add the latest observation and its canonical digest to the internal prepared
  mutation input.
- Revalidate exact observation, intent, operation, and plan correspondence at
  reservation and while the owned child runs.
- Extend executable staged and registered-child regressions.

## Non-Goals

- No live GitHub call, token lookup, target setting, or branch mutation.
- No claim of atomic server predicate, protected host/store, or operational
  provider qualification.
- No adoption of the other six imported `UR-INT-*` proposals.
- No full broker completion or activation.

## Progress

- [x] Identify the missing observation-to-child binding in current source.
- [x] Admit this bounded child and map source aliases to stable AIDE IDs.
- [x] Implement exact observation carriage and repeated authorization checks.
- [x] Add adversarial executable tests.
- [x] Run focused and broader affected validation.
- [x] Record exact evidence and prepare the source checkpoint for publication.

## Validation

Run the staged broker and registered bridge suites, including missing/changed
observation refusal and acknowledgement-versus-closeout behavior. Run queue and
repository validation, scoped diff checks, and structured commit checks. Do not
translate fixture success into operational provider or host qualification.

## Recovery

Before commit, revert only this WorkUnit's explicit paths if tests fail. After a
published checkpoint, fix forward on the same task branch; do not rewrite shared
history or replay an uncertain external effect. This slice performs no external
effect.

## Decisions And Discoveries

- The staged ledger already persisted the exact observation digest that selected
  each mutation. The missing boundary was carriage of that same observation into
  the registered child request and revalidation against the durable latest row.
- A mutation acknowledgement remains `pending`. Only a later authoritative
  observation can select the next stage or prove integration.
- The Windows symlink regression remains unrun on this host because the current
  identity lacks symlink-creation privilege; all other affected tests passed.

## Retrospective

The bridge now binds each mutation envelope to the exact latest observation,
its digest, the durable stage intent, and the pure stage decision before child
execution and during its bounded lifetime. Adversarial tests refuse missing,
changed, wrong-actor, wrong-stage, and stale observations without creating a
provider-call directory. The parent broker remains running because operational
provider, protected host/store, credential, target-policy, and hosted acceptance
work is still open.
