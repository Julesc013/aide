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
2. Completed: queue packet and policy/schema foundations.
3. Completed: AIDE Lite command implementation and generated upgrade outputs.
4. Completed: unit tests and golden tasks.
5. Completed: documentation and export-pack sync.
6. Completed: final validation and review-gated evidence.

## Verification Intent

Ran the Q45 upgrade commands, AIDE Lite validation/test/selftest surfaces,
export-pack and pack-status, targeted unit tests, diff checks, core unittest
suites where present, and secret scans. Full `eval run` and changelog preview
were not rerun in the final pass because they refresh generated outputs outside
Q45 scope; Q45 golden tasks and AIDE Lite internal eval coverage passed. The
pre-existing generated manifest warning and the `core/gateway/tests` timeout
are recorded honestly.

## Exit Criteria

Q45 status is `needs_review`, upgrade observation/source/comparison/plan/dry-run
artifacts exist and validate, all operations remain no-apply and
non-overwriting/non-deleting, target-specific state preservation rules exist,
source-generated state is not exported as target truth, evidence is complete,
and no forbidden mutation occurs.
