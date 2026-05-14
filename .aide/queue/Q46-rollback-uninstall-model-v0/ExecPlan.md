# Q46 ExecPlan: Rollback / Uninstall Model v0

## Objective

Create deterministic rollback and uninstall observation, ownership-aware
classification, preservation-first planning, dry-run, validation, and evidence
infrastructure without rollback or uninstall apply behavior.

## Scope

- Add Q46 rollback policies for rollback classes, safety, and verification.
- Add Q46 uninstall policies for uninstall classes, safety, and verification.
- Add `.aide/rollback` and `.aide/uninstall` schemas and generated no-apply
  planning outputs.
- Extend AIDE Lite with rollback and uninstall `observe`, `plan`, `dry-run`,
  `validate`, `status`, `explain`, and `classes` commands.
- Add tests, golden tasks, documentation, export-pack support, and evidence.

## Boundaries

- No target repo mutation.
- No rollback apply mode.
- No uninstall apply mode.
- No install, repair, or upgrade apply mode.
- No file overwrites.
- No file moves or deletes.
- No reference rewrites.
- No managed-section removal.
- No provider, model, or network calls.
- No branch, GitHub, tag, release, CI, or workflow mutation.

## Milestones

1. Completed: baseline repo and Q45 dependency inspection.
2. In progress: queue packet foundation.
3. Pending: rollback/uninstall policies and schemas.
4. Pending: AIDE Lite command implementation and generated outputs.
5. Pending: unit tests and golden tasks.
6. Pending: documentation and export-pack sync.
7. Pending: final validation and review-gated evidence.

## Verification Intent

Run the Q46 rollback and uninstall commands, AIDE Lite validation/test/selftest
surfaces, export-pack and pack-status, targeted unit tests, diff checks, core
unittest suites where present, and secret scans. Record pre-existing warnings
and slow or timed-out suites honestly.

## Exit Criteria

Q46 status is `needs_review`; rollback/uninstall observation, plan, dry-run, and
verification artifacts exist and validate; all operations remain no-apply and
non-overwriting/non-deleting; target-specific state and unknown ownership are
preserved or blocked for manual review; source-generated rollback/uninstall
outputs are not exported as target truth; evidence is complete; and no
forbidden mutation occurs.
