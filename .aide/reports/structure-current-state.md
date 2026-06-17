# Structure Current State

- task_id: AIDE-STRUCTURE-00-current-truth-and-root-authority-audit
- generated_at: 2026-06-18
- source_commit: 53405366d5143ba540ad801352743d8472ff8288
- report_only: true
- mutation_performed: false
- file_moves: false
- file_deletes: false
- reference_rewrites: false
- provider_or_model_calls: none
- network_calls: none
- branch_mutation: false
- target_repo_mutation: false

## Current Truth

- Task OS reports 141 queue items and selects `AIDE-STRUCTURE-00-current-truth-and-root-authority-audit` as the latest task.
- Repo intelligence reports 5,136 tracked files, 0 unknown classifications, 943 generated files, 2,687 evidence files, and 608 orphan candidates.
- Root inventory reports 22 tracked roots, 3 mixed roots, 19 unknown/review-required roots, 15 high-risk roots, and 5,047 review-required files.
- Root fates remain candidate-only: 4,822 `keep` and 314 `unknown`.
- Refactor map status reports 0 move entries, 20 salvage entries, 0 path aliases, and 40 reference rewrite candidates.
- Reconciler reports 4 warning findings and no repair authority.

## Tracked Roots

`.agents`, `.aide`, `.aide.local.example`, `.codex`, `bridges`, `core`, `docs`,
`environments`, `evals`, `fixtures`, `governance`, `hosts`, `inventory`,
`labs`, `matrices`, `packaging`, `platforms`, `repo-root`, `research`,
`scripts`, `shared`, and `specs`.

Local-only roots such as `.git`, `.aide.local`, and `tmp` were observed in the
filesystem listing but are not tracked root-authority candidates.

## Drift Findings

1. Previously cited file counts are stale. The live repo inventory now reports
   5,136 tracked files, not the older 1,781 or 2,598-file figures.
2. The generated latest task packet now points at this audit, while Reconciler
   still flags it as stale relative to accepted OKF queue routing. The task-local
   `task.yaml` is the canonical allowlist.
3. OKF current-state pages and OKF reports retain pre-acceptance next-task
   routing, including `AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01`, while queue truth
   has moved through Reconciler and CapabilityManifest work.
4. README still labels Reconciler, CapabilityManifest, ConformanceProfile, and
   PatchTransaction as planned. Queue and implementation records have advanced
   beyond that for Reconciler, CapabilityManifest build/check, transaction model,
   managed-section patcher, scoped transaction executor, and lifecycle fixture
   slices. This audit records the drift only.
5. Q37 has stale task-packet metadata: `task.yaml` says `running`, while
   `status.yaml`, the queue index, and Task OS status report `needs_review`.
6. `git plan` is blocked by a dirty tree because this task has created audit
   artifacts. That is expected and must be classified before commit.

## Authority Conclusion

The repo does not need immediate directory shuffling. It needs root authority
contracts and stale-status reconciliation before any no-apply map can become a
future reviewed move batch.

Generated outputs remain evidence or projections, not source truth. Root and
refactor reports are advisory and no-apply. Orphan candidates, unknown fates,
salvage candidates, and rewrite candidates are not deletion or rewrite approval.

## Recommended Follow-Up

1. `AIDE-STRUCTURE-01-root-authority-contracts`
2. `AIDE-STRUCTURE-02-status-doc-sync`
3. `AIDE-STRUCTURE-03-shared-platforms-research-specs-fate-map`
4. `AIDE-STRUCTURE-04-dot-tool-roots-interop-policy`
5. `AIDE-STRUCTURE-05-tools-tests-examples-root-plan`
