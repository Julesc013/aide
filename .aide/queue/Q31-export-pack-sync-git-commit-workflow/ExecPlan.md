# Q31 ExecPlan - Export Pack Sync for Git Commit Workflow

## Purpose

Q31 makes the portable `aide-lite-pack-v0` carry the target-safe governance
introduced by Q27 through Q30. The pack should export commit discipline,
WorkUnit recovery, generic Git workflow policy, and dry-run Git helper support
without exporting AIDE source queue history, source branch-state reports,
generated context, local state, secrets, raw prompts, or raw responses.

## Scope

- Create the Q31 queue packet and evidence set.
- Update export/import policy anchors for Q27-Q30 governance.
- Harden export and safe import boundaries for portable governance.
- Add Q31 golden tasks and tests for inclusion, exclusion, and fixture import.
- Regenerate `aide-lite-pack-v0`.
- Validate an imported temporary fixture can run commit/task/Git commands.
- Update compact docs and agent guidance for target sync readiness.
- Regenerate the Q32 compact task packet.

## Non-Goals

- No Eureka or Dominium mutation.
- No live pack installation into target repositories.
- No live branch creation, deletion, merge, push, prune, or promotion.
- No GitHub API, branch protection, CI, release, installer, provider/model,
  Gateway forwarding, or network work.

## Dependencies

- Q27 commit discipline and WorkUnit recovery: present and `needs_review`.
- Q28 Git workflow policy: present and `needs_review`.
- Q29 dry-run Git helpers: present and `needs_review`.
- Q30 AIDE dev/main policy sync: present and `needs_review`.
- Q25 import safety convention: pack-status passes and safe import skips broad
  source roots by default.

## Implementation Steps

1. Record baseline Git, Harness, AIDE Lite, Git helper, pack, and unit-test
   results.
2. Create Q31 queue packet and set status to running.
3. Update `.aide/policies/export-import.yaml` with portable governance include
   classes and explicit source-state exclusions.
4. Extend AIDE Lite export validation, golden tasks, and fixture-import tests.
5. Update portable guidance and reference docs for Q31 target import behavior.
6. Regenerate the export pack, changelog previews, Git detection reports, and
   Q32 latest task packet.
7. Run final validation, secret scan, fixture import validation, and
   pack-status.
8. Write evidence and set Q31 to `needs_review`.
9. Commit coherent slices using Q27 commit discipline.

## Validation Intent

- AIDE Harness validate/doctor/self-check.
- AIDE Lite validate/test/selftest/eval run.
- Commit checker and changelog preview.
- Git report-only commands and dry-run helpers.
- Export-pack and pack-status.
- Fixture import and imported governance commands.
- Full `.aide/scripts/tests` discovery.
- Core Harness/Compat/Gateway/Provider tests.
- Targeted secret scan.

## Review Gate

Q31 ends at `needs_review`, not `passed`.
