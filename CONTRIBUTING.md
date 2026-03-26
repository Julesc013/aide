# Contributing To AIDE

## Who This Guide Is For

This guide is for human contributors and agentic contributors making scoped changes inside the AIDE repository.

## Start Here

Before editing:

1. Inspect the repository state.
2. Read `AGENTS.md` and the relevant governing or architecture docs for the task.
3. Confirm the allowed paths for the current work.
4. Write a short plan for any multi-file or policy-sensitive task.

## Repository Orientation

Use the directory that matches the nature of the change:

- `governance/`: repository law and policy
- `inventory/`: canonical ids, enums, versions, and machine-readable ecosystem records
- `matrices/`: current support, capability, feature, test, packaging, and platform posture
- `specs/`: architecture contracts and boot-slice specifications
- `shared/`: reusable shared-core implementation, schemas, and tests
- `hosts/`: thin host-lane proofs, blocked records, and lane-local wrappers
- `research/`: source-backed ecosystem facts and unresolved-item registers
- `environments/`: concrete runnable or reconstructable environment control-plane records
- `labs/`: prototypes, blocked work, and archival experimental records
- `evals/`: verification models, run records, and audit-style reports
- `packaging/`: artifact and release-shape control plane
- `scripts/`: repeatable repository operations and maintenance assets
- `.agents/`: repo-local skills and narrow operational guidance

## Choose The Right Place For A Change

- Update `governance/` only when repository law or core doctrine is actually changing.
- Update `inventory/` when ids, version records, enums, or canonical machine-readable records need to change.
- Update `matrices/` when support or capability posture, feature coverage, or verification posture changes.
- Update `specs/` when durable architecture or contract expectations change.
- Update `shared/` only for reusable cross-host behavior.
- Update `hosts/` only for lane-local proof artifacts, wrappers, manifests, or blocked or deferred records.
- Update `research/` only for source-backed ecosystem facts, inferences, or unresolved items.
- Update `scripts/` and `.agents/` only for repeatable repo operations, maintenance support, or narrow reusable instructions.

## Keep Diffs Scoped

- Edit the smallest coherent set of files that satisfies the task.
- Do not silently expand scope because an adjacent cleanup seems appealing.
- If a cross-cutting edit is necessary for coherence, keep it narrow and record the reason in `IMPLEMENT.md`.
- Do not mix product implementation, policy changes, and broad documentation rewrites in one uncontrolled diff.

## Root Control-Plane Updates

Substantial work should update the control-plane files in the same change set:

- `PLANS.md`: add or refine the plan entry when a new multi-step phase or milestone is completed
- `IMPLEMENT.md`: record what changed, why it changed, tradeoffs, verification, and remaining blockers or deferrals
- `DOCUMENTATION.md`: update indexing guidance when authoritative docs or repo structure change

Use these files to describe reality, not aspiration.

## Blocked, Deferred, And Unverified Work

- Use `blocked` when a lane or task cannot honestly meet its minimum accepted proof because of a concrete blocker.
- Use `deferred` when richer work is intentionally postponed after the current accepted proof succeeds.
- Use `unverified` or equivalent explicit language when a claim is meaningful but has not yet been confirmed.
- Do not collapse blocked work into silence.
- Do not turn missing verification into implied success.

## Naming And Coverage Rules

- Keep directory names based on compatibility technology or host contract.
- Do not add exact versions, date ranges, or vague eras to source directory names.
- Put exact version coverage in manifests, inventory records, and matrices.

## Adding Future Host Families Or Adapter Lanes

Before promoting a candidate family into `hosts/` or adding a new adapter lane:

1. Ensure the research corpus and backlog records justify the promotion.
2. Keep candidate families distinct from committed families.
3. Prefer contract-based lane names over version-based folder names.
4. Update inventory, matrices, specs, and documentation together.
5. Record unresolved blockers and capability ceilings explicitly.

Do not create new committed host lanes only because a family is interesting.

## Verification Expectations

- Run the strongest honest verification available for the change.
- Prefer executable verification when runnable behavior exists.
- Use structural verification when runtime verification is not possible.
- Record exactly what was run and what was not run.
- Do not describe unrun checks as passed.

## Commit Discipline

- Keep commits scoped to the finished task or phase.
- Do not sweep unrelated local changes into the commit.
- Preserve unrelated user changes unless the task explicitly requires touching them.
