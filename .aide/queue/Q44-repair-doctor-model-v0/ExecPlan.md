# Q44 ExecPlan: Repair / Doctor Model v0

## Objective

Create deterministic repair observation, diagnosis, class mapping, planning,
dry-run, doctor-report, and verification infrastructure without repair apply
behavior.

## Scope

- Add Q44 repair policies for classes, safety, detection, verification, and doctor integration.
- Add `.aide/repair` schemas and generated no-apply repair planning outputs.
- Extend AIDE Lite with `repair observe`, `diagnose`, `plan`, `dry-run`,
  `validate`, `status`, `explain`, `classes`, and `doctor`.
- Add tests, golden tasks, documentation, export-pack support, and evidence.

## Boundaries

- No target repo mutation.
- No repair apply mode.
- No install, upgrade, rollback, or uninstall apply mode.
- No file overwrites.
- No file moves or deletes.
- No reference rewrites.
- No automatic migrations.
- No provider, model, or network calls.
- No branch, GitHub, tag, release, CI, or workflow mutation.

## Milestones

1. Completed: baseline repo and Q43 dependency inspection.
2. In progress: queue packet and policy/schema foundations.
3. Pending: AIDE Lite command implementation and generated repair outputs.
4. Pending: unit tests and golden tasks.
5. Pending: documentation and export-pack sync.
6. Pending: final validation and review-gated evidence.

## Verification Intent

Run the Q44 repair commands, AIDE Lite validation/test/eval surfaces,
export-pack and pack-status, targeted unit tests, diff checks, commit checks,
core unittest suites where present, and secret scan. Record residual
pre-existing warnings honestly.

## Exit Criteria

Q44 status is `needs_review`, repair observation/diagnosis/plan/dry-run
artifacts exist and validate, all operations remain no-apply and
non-overwriting/non-deleting, target-specific state preservation rules exist,
source-generated state is not exported as target truth, evidence is complete,
and no forbidden mutation occurs.
