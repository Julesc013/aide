# Current Truth And Root Authority Audit

This note records the check-only result for
`AIDE-STRUCTURE-00-current-truth-and-root-authority-audit`.

## Verdict

Do not move files yet. The live repo already has no-apply repo intelligence,
root recycling, and refactor-map machinery, and the current reports show enough
drift that immediate restructuring would be premature.

The next safe step is a root authority contract task, followed by a docs/status
sync task. File moves, root creation, reference rewrites, and archive decisions
need separate reviewed no-apply maps before any future apply phase.

## Live Counts

- Repo intelligence: 5,136 tracked files, 0 unknown classifications, 943
  generated files, 2,687 evidence files, and 608 orphan candidates.
- Root inventory: 22 tracked roots, 3 mixed roots, 15 high-risk roots, and
  5,047 review-required files.
- Root fates: 4,822 `keep`, 314 `unknown`.
- Refactor map: 0 move entries, 20 salvage entries, 0 path aliases, 40
  reference rewrite candidates.
- Task OS: 141 queue items, with this structure audit selected as the latest
  task.
- Reconciler: 4 warning findings, report-only, no repair authority.

## Current Drift To Carry Forward

- The generated latest task packet points at this audit, while Reconciler still
  flags it as stale relative to accepted OKF queue routing. Queue-local
  `task.yaml` remains the authority.
- OKF current-state pages and OKF build reports retain pre-acceptance next-task
  routing.
- README still describes Reconciler, CapabilityManifest, ConformanceProfile,
  and PatchTransaction as planned, while live queue evidence has advanced for
  Reconciler, CapabilityManifest build/check, transaction model, managed-section
  patcher, scoped transaction executor, and lifecycle fixture slices.
- Q37 has stale task-packet metadata: its `task.yaml` says `running`, while
  live status surfaces say `needs_review`.
- Git helper planning blocks on the task-owned dirty tree until these audit
  artifacts are classified and committed.

## Root Authority Direction

- `.aide` is the repo-local AIDE contract and control-plane state root.
- `core` is implementation library code, not canonical repo state.
- `governance` is human-readable law; `.aide/policies` is machine-readable law.
- `docs` explains; it does not replace queue, protocol, policy, evidence, or
  generated report truth.
- `inventory` records facts; `matrices` provides cross-cutting views.
- `hosts` is for host integrations; `bridges` is for target-repo adoption.
- `scripts` should stay thin wrappers.
- `shared`, `platforms`, `research`, and `specs` need fate maps before movement.
- `.agents` and `.codex` need explicit interop/projection policy.
- `tools`, `tests`, `examples`, and `archive` should not be created for
  symmetry; each needs a reviewed justification.

## Next Tasks

1. `AIDE-STRUCTURE-01-root-authority-contracts`
2. `AIDE-STRUCTURE-02-status-doc-sync`
3. `AIDE-STRUCTURE-03-shared-platforms-research-specs-fate-map`
4. `AIDE-STRUCTURE-04-dot-tool-roots-interop-policy`
5. `AIDE-STRUCTURE-05-tools-tests-examples-root-plan`

## Boundary

This note is planning evidence. It does not authorize file moves, deletes,
reference rewrites, path aliases, shims, new top-level roots, source-truth
promotion for generated outputs, branch mutation, target-repo mutation,
provider/model calls, network calls, release work, or product readiness claims.
