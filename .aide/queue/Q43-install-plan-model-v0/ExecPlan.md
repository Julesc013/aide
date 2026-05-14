# Q43 ExecPlan: Install Plan Model v0

## Objective

Create deterministic install observation, planning, dry-run, preservation,
ownership-ledger, conflict-report, and verification infrastructure without
install apply behavior.

## Scope

- Add Q43 install policies for preservation, ownership, conflicts, migrations,
  and verification.
- Add `.aide/install` schemas and generated no-apply install planning outputs.
- Extend AIDE Lite with `install observe`, `plan`, `dry-run`, `validate`,
  `status`, `explain`, `ownership`, and `conflicts`.
- Add tests, golden tasks, documentation, export-pack support, and evidence.

## Boundaries

- No target repo mutation.
- No install apply mode.
- No file overwrites.
- No file moves or deletes.
- No reference rewrites.
- No automatic migrations.
- No provider, model, or network calls.
- No branch, GitHub, tag, release, CI, or workflow mutation.

## Milestones

1. In progress: queue packet and dependency inspection.
2. Pending: policies and schemas.
3. Pending: AIDE Lite command implementation and generated install outputs.
4. Pending: unit tests and golden tasks.
5. Pending: documentation and export-pack sync.
6. Pending: final validation and review-gated evidence.

## Verification Intent

Run the Q43 install commands, AIDE Lite validation/test/eval surfaces,
export-pack and pack-status, targeted unit tests, diff checks, commit checks,
core unittest suites where present, and secret scan. Record residual
pre-existing warnings or timeouts honestly.

## Exit Criteria

Q43 status is `needs_review`, install observation/plan/dry-run artifacts exist
and validate, all operations remain no-apply and non-overwriting,
target-specific state preservation rules exist, source-generated state is not
exported as target truth, evidence is complete, and no forbidden mutation
occurs.
