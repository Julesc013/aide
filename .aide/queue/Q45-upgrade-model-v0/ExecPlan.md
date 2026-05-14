# Q45 ExecPlan: Upgrade Model v0

## Objective

Create deterministic upgrade observation, source-pack comparison,
compatibility classification, preservation-first planning, dry-run,
validation, and evidence infrastructure without upgrade apply behavior.

## Scope

- Add Q45 upgrade policies for compatibility, preservation, conflicts,
  migrations, and verification.
- Add `.aide/upgrade` schemas and generated no-apply upgrade planning outputs.
- Extend AIDE Lite with `upgrade observe-current`, `observe-source`,
  `compare`, `plan`, `dry-run`, `validate`, `status`, `explain`,
  `compatibility`, `conflicts`, and `migrations`.
- Add tests, golden tasks, documentation, export-pack support, and evidence.

## Boundaries

- No target repo mutation.
- No upgrade apply mode.
- No install, repair, rollback, or uninstall apply mode.
- No file overwrites.
- No file moves or deletes.
- No reference rewrites.
- No automatic migrations.
- No provider, model, or network calls.
- No branch, GitHub, tag, release, CI, or workflow mutation.

## Milestones

1. Completed: baseline repo and Q44 dependency inspection.
2. In progress: queue packet and policy/schema foundations.
3. Pending: AIDE Lite command implementation and generated upgrade outputs.
4. Pending: unit tests and golden tasks.
5. Pending: documentation and export-pack sync.
6. Pending: final validation and review-gated evidence.

## Verification Intent

Run the Q45 upgrade commands, AIDE Lite validation/test/eval surfaces,
export-pack and pack-status, targeted unit tests, diff checks, commit checks,
core unittest suites where present, and secret scan. Record residual
pre-existing warnings honestly.

## Exit Criteria

Q45 status is `needs_review`, upgrade observation/source/comparison/plan/dry-run
artifacts exist and validate, all operations remain no-apply and
non-overwriting/non-deleting, target-specific state preservation rules exist,
source-generated state is not exported as target truth, evidence is complete,
and no forbidden mutation occurs.
