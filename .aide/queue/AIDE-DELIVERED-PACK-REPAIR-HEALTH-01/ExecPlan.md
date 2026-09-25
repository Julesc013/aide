# ExecPlan: installed Lite repair health

## Objective and scope

Close the mandatory diagnosis gap for a delivered Lite installation. A user
should be able to inspect receipt-owned files in an installed target without
the development checkout and understand which one-file missing state the
existing bounded repair command can safely restore. The command is read-only;
it must not turn unknown or locally changed bytes into ownership authority.

Admitted paths are the Lite importer/repair CLI, its importer tests, the
portable guide, this WorkUnit, queue index and PLANS/IMPLEMENT. Only the root
controller writes shared Git refs, queue index and generated pack/release
state. This source stream uses a separate worktree and no real target.

## Dependencies and evidence

- Base source is the independently accepted-with-notes three-way update
  `12758e07373f8bfedee667715df04f8caaf1de23`, tree
  `2cf08c4d846b4413a748a0a037f7f86ce1600388`. Its full suite and dev
  integration are still pending; this task cannot close that dependency.
- External read-only repair catalogue:
  `D:/Projects/AIDE/_review_scratch/lite-repair-catalogue-d4b67c96-readonly.md`,
  SHA-256 `57d78c1b0fb33e76d15362ee5c642ac7fc619d62f15b28a29102d6ebbc10adf7`.
- External test-only extracted ZIP probe:
  `D:/Projects/AIDE/_review_scratch/probe_portable_repair_health.py`, SHA-256
  `e154519a93e1183ae7939070f4cc0989d79f84212d680c001ee94cf5d4b03b61`.
  Its first missing-file case was red because the proposed CLI is absent;
  full details and unrun cases are in the handoff SHA-256
  `453c492c8c7ef31a615fa27bbf40d8d47c116dc4c320dbf5cadb1fe495272e28`.

## Execution and verification

1. Characterize current `repair-owned-file`, receipt v1/v2, intent and target
   path contracts. Run/adapt the test-only red probe on exact admitted source.
2. Implement a read-only health report with a versioned JSON schema, exact
   pack/target identity, observed file/section states, pending-intent flags,
   reason, next action and `network_calls: false`. Reuse existing validators
   and verified path reads; do not add a second repair effect engine.
3. Test missing receipt-owned file, direct edit, unknown or hard-linked path,
   invalid receipt, pending repair/import/removal intent, v1/v2 overlay and
   disabled feature. A missing file is repair eligible only when the existing
   exact-pack one-file repair preview independently permits it.
4. Run affected source tests and extracted CLI disposable consumers. Obtain
   independent review of exact source/security changes. Later combine with
   qualified three-way update and regenerate artifacts once from combined
   source, then obtain exact effect review before dev integration.

## Recovery and progress

External probes and test logs remain outside the repo with exact hashes and
exit codes. Any interrupted consumer leaves its target under disposable
scratch for inspection; do not replay an uncertain effect. No generated
artifact or real target is changed by this admission.

- [x] Owner campaign delegation and source dependency identified.
- [x] Read-only catalogue and one extracted-CLI red probe prepared externally.
- [x] Bounded task branch/worktree admitted.
- [x] Admitted source rejected `repair-health` as an unknown command (CLI exit 2); implemented read-only inspection and ran the frozen source-focused tests, including extracted ZIP consumer tests. See `evidence/source-candidate.md`.
- [x] Independently review frozen source `03c5e7f8`; it returned REQUEST_CHANGES for forged receipt baseline and source-to-target mapping. Superseding source and no-write regressions are in `evidence/receipt-baseline-repair.md`.
- [x] Independently rereview `486aa2bd`; it returned REQUEST_CHANGES for a valid CRLF pack template whose raw block hash was normalized before comparison. The exact report and repair are in `evidence/crlf-template-repair.md`.
- [ ] Independently rereview the CRLF repair; combine and qualify delivered bytes. Keep this WorkUnit running until those gates close.
