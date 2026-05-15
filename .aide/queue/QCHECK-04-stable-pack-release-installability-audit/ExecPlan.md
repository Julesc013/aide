# QCHECK-04 ExecPlan: Stable Pack Release Installability Audit

## Objective

Produce an evidence-based checkpoint before Q49 that classifies Q36-Q48,
validates the export pack, release bundle, release draft, no-apply boundaries,
fixture installability, target-handoff readiness, and publication boundary.

## Scope

- Create QCHECK-04 audit artifacts under this queue directory.
- Update `.aide/queue/index.yaml` to track the checkpoint.
- Run local validation and fixture checks only.
- Generate the Q49 task packet after the audit if validation allows it.

## Boundaries

- No Q49 execution.
- No Dominium or Eureka mutation.
- No GitHub API, tags, releases, uploads, publishing, branch mutation, CI
  installation, provider/model calls, network fetches, or target installs.
- No install, repair, upgrade, rollback, uninstall, refactor, root, or tool
  apply behavior.

## Plan

1. Inspect git state, governing docs, queue state, Q36-Q48 evidence, export
   pack, release bundle, and release draft artifacts.
2. Run local validation and command-surface checks, recording pass/warn/fail
   outcomes and unavailable commands.
3. Inspect export pack and release archives for checksum validity, forbidden
   paths, and source-state leakage.
4. Run temporary fixture simulations for fresh, existing-state, and unsafe
   target repos using only local pack files and no apply mode.
5. Write the audit reports and evidence.
6. Regenerate the Q49 task packet if appropriate.
7. Run final validation and stop at `needs_review`.

## Progress

- [x] Git state, root docs, queue state, Q36-Q48 evidence, export pack, release bundle, and release draft inspected.
- [x] Local validation and command-surface checks run.
- [x] Export pack and release archives inspected for checksums, forbidden paths, and leakage.
- [x] Fresh, existing-state, and unsafe fixture simulations run under system temp.
- [x] Audit reports and evidence written.
- [x] Final validation rerun completed.
- [ ] Audit commit completed.

## Verification Intent

Use AIDE harness, AIDE Lite validation, pack-status, release validation, release
draft validation, lifecycle model validation, targeted tests, archive extraction
checks, fixture checks, secret/local-state scans, and commit discipline.

## Exit Criteria

QCHECK-04 status is `needs_review`; required reports and evidence exist;
warnings are classified; target-handoff recommendation is explicit; and no
forbidden publication, network, branch, target, or apply action occurred.
