# QCHECK-03 Ultimate AIDE Readiness Audit

## 1. Executive Verdict

Verdict: `PASS_AFTER_Q35_FIX`.

Current reliable phase: Q35. AIDE has passing local governance,
token-survival, export-pack, changelog, commit discipline, WorkUnit recovery,
dry-run Git helper scaffolding, and report-only GitHub/CI advisory support.

Original audit finding: Q35 was missing. Resolution: Q35 now has a queue
packet, status, evidence, policy, generated `.aide/github` reports, tests,
golden tasks, docs, export-pack support, and AIDE Lite `github` commands.

Q36 can now be planned from repo-local state. It remains a future queue item and
must not execute raw prompts directly.

Immediate next action: run Q36 Intent Compiler and Prompt Normalization v0.

## 2. Binding Goal Assessment

| Goal | Assessment | Evidence |
|---|---|---|
| Token reduction | Passing for compact packets; not exact billing proof. | AIDE latest audit-derived packet is 3,735 chars / 934 approximate tokens. Eureka Q32 reports 98.5 percent reduction. Dominium Q33 reports about 98.9 percent reduction against a doctrine-heavy baseline. |
| Equivalent quality | Partially evidenced for governance tasks through deterministic validation and golden tasks. Not arbitrary product quality proof. | `eval run` PASS 30/30, Harness PASS 149 info / 0 warnings / 0 errors, core tests pass. |
| Additive upgrade | Good policy posture; installer/upgrade rollback not yet implemented. | Export/import policy excludes source state and preserves target-specific memory, but install/upgrade/rollback commands are missing. |
| Target preservation | Good in Q31 pack and target Q32/Q33 evidence, but target sync remains needs-review. | Eureka and Dominium sync packets preserve target memory, queues, generated reports, and local doctrine. |
| Tool absorption | Policy need is clear; implementation missing. | Dominium has XStack/AuditX/RepoX/TestX roots and data maps; AIDE has no absorption registry yet. |
| Vague prompt normalization | Not implemented as a first-class compiler. | Q27 recovery helps repeated/out-of-order prompts, but Q36 must add intent normalization. |
| Install/rollback readiness | Not ready for automatic stable install. | `import-pack --dry-run` exists; observe/plan/apply/verify/repair/upgrade/rollback/uninstall schemas are missing. |

## 3. Current AIDE State

- Branch: `main`.
- Commit at original audit: `6246811cf02ece09bd25b53ce0625919db658f51`.
- Remote: `origin https://github.com/Julesc013/aide.git`.
- Local branch topology: local `main` plus `origin/main`; no local or remote
  `dev` detected.
- Ahead/behind known from Git helper: local `main` is 39 commits ahead of
  `origin/main`.
- Tags: none.
- Initial worktree: clean.
- Audit/generated worktree after command generation: dirty by allowed generated
  reports and this checkpoint.
- Queue: Q35 is now present and passed; Q36 is present as the next pending queue item.
- Q35: implemented report-only advisory.
- Export pack: `pack-status` PASS, checksums valid, boundary PASS, provenance
  `DIRTY_SOURCE_RECORDED`.

## 4. Q35 Status

Q35 is `passed`.

Evidence:

- `.aide/queue/Q35-github-protection-ci-advisory-v0/` exists.
- `.aide/policies/github-protection.yaml`, `.aide/policies/ci-gates.yaml`,
  `.aide/policies/branch-protection.yaml`, and `.aide/github/**` exist.
- `py -3 .aide/scripts/aide_lite.py github advisory` and `github validate`
  pass without GitHub API, CI, branch, tag, release, provider, model, or
  network mutation.

Recommendation: run Q36 next.

## 5. Governance Readiness Matrix

| Area | Implemented | Tested | Exported | Target-safe | Limitations | Next action |
|---|---:|---:|---:|---:|---|---|
| Commit discipline | yes | yes | yes | yes | Old history can remain malformed. | Keep checker opt-in/hook opt-in. |
| WorkUnit recovery | yes | yes | yes | yes | Report-first; no autonomous broad repair. | Q36 should compile raw prompts into WorkUnits. |
| Task recovery | yes | yes | yes | yes | Q36 is planned, not implemented. | Run Q36 next. |
| Git workflow | yes | yes | yes | yes | No `dev` branch exists in AIDE. | Q35/Q36 must not mutate branches. |
| Git helpers | yes | yes | yes | yes | Dry-run default; live mutation not exercised. | Keep `--apply` operator-gated. |
| Changelog preview | yes | yes | yes | yes | 8 malformed/legacy commits reported for review. | Keep preview-only until release tooling. |
| GitHub/CI advisory | yes | yes | yes | yes | advisory only; no active GitHub settings or workflows. | Future apply phase needs rollback and operator approval. |
| Export pack | yes | yes | yes | yes | Provenance records dirty source when generated during audit. | Add install/upgrade/rollback schemas later. |
| Target sync | target-side partial | target evidence exists | n/a | partial | Q32/Q33 remain `needs_review` in targets. | Review target sync packets before product work. |

## 6. AIDE Pack Installability

Current pack readiness:

- Portable governance files are present.
- Source-specific queue, memory, context, reports, Git detection/helper plans,
  changelog previews, `.aide.local`, raw prompts, raw responses, and secrets are
  excluded.
- `pack-status` passes.
- Fixture import support exists from Q31 evidence.

Installability gaps:

- No stable installer command with observe/plan/apply/verify lifecycle.
- No ownership ledger for imported files.
- No target conflict classification schema beyond current import dry-run output.
- No upgrade plan schema.
- No repair plan schema.
- No rollback plan schema.
- No uninstall plan schema.
- No release bundle manifest or GitHub release draft integration.

Verdict: the pack is safe for controlled targeted sync and dry-run import. It
is not yet a stable automatic installer/upgrader/rollback control plane.

## 7. Target Preservation Doctrine

AIDE must preserve target-specific truth:

- Eureka: `.aide/memory/**`, `.aide/queue/EUREKA-AIDE-*`, Eureka-specific
  golden tasks, architecture boundary checks, generated target packets, product
  boundaries, and manual `AGENTS.md` content.
- Dominium: `AGENTS.md`, canon/doctrine docs, doctrine refs, `.aide/memory/**`,
  `.aide/context/dominium-doctrine-refs.md`, `.aide/queue/DOMINIUM-AIDE-*`,
  generated target packets, XStack/AuditX/RepoX/TestX systems, and product
  roots.
- All targets: manual content, target queues, target-generated context, local
  caches, `.aide.local`, existing command matrices, and existing validators.

No target repo should inherit AIDE source generated branch reports or AIDE
source queue history as target truth.

## 8. Existing Tool Absorption Plan

Generic model:

`discover -> classify -> wrap -> adapt -> migrate -> retire with evidence`.

| System | Target | Likely fate | First AIDE action |
|---|---|---|---|
| XStack | Dominium | preserve and wrap | Inventory entrypoint, profiles, outputs, cache, and authority boundaries. |
| AuditX | Dominium | preserve and wrap | Map semantic drift reports into AIDE evidence packets. |
| RepoX | Dominium | preserve and wrap | Map static repo invariants into AIDE validation gates. |
| TestX | Dominium | preserve and wrap | Map FAST/STRICT/FULL profiles into AIDE task validation levels. |
| BuildX-like release/update tooling | Dominium | preserve and classify | Identify release/trust surfaces before any install or release work. |
| Eureka architecture checks | Eureka | preserve and wrap | Treat `scripts/check_architecture_boundaries.py` as a target validator. |
| Eureka WorkUnit/OBS systems | Eureka | preserve and classify | Map existing WorkUnit seed/review docs to AIDE WorkUnit language. |
| Command matrices | both | preserve and adapt | Register as command providers, not delete. |
| Root inventories | both | preserve and compare | Feed Q37/Q40 repo intelligence and root recycling ledgers. |
| Old task catalogs | both | preserve and map | Add alias/migration records before retirement. |

## 9. Intent + Repo Intelligence + Quality Plan

Q36 should add the intent compiler. It must normalize vague or broad prompts
into bounded WorkUnits, classify task/risk, reconcile queue state, inspect
branch role, select context, specify evidence, and reject or split unsafe work.

Q37 should build the repo intelligence index. It must collect file inventory,
ownership, dependencies, tests, docs, generated status, source-of-truth anchors,
and target tool entrypoints.

Q38 should build the file quality ledger. It must flag stale docs, orphan files,
duplicate policies, missing tests, generated/manual boundary issues, path drift,
and unclear ownership.

## 10. Refactor / Root Recycling Plan

Q39-Q42 should create policy and dry-run-only planning for refactors, root
recycling, migration ledgers, tool absorption ledgers, move maps, salvage maps,
path aliases, and root/tool inventory commands. They must not move roots or
delete tools.

## 11. Install / Upgrade / Rollback / Release Plan

Q43-Q48 should build installer-adjacent control plane pieces:

- install preflight and ownership ledger;
- observe/plan/dry-run installer;
- upgrade/repair/rollback planner;
- uninstall planner;
- stable pack release bundle draft;
- GitHub release draft integration.

No publication, tags, GitHub Releases, CI installation, or automatic branch
protection should occur in these phases.

## 12. Dominium Fresh Install Plan

Shortest safe path to a stable Dominium AIDE Lite control plane:

1. Complete Q35 in AIDE.
2. Build Q43-Q45 install/upgrade/repair/rollback schemas and dry-run commands.
3. Run Q49 Dominium preflight read-only, preserving doctrine and XStack.
4. Run Q50 Dominium stable pack upgrade dry-run.
5. Run Q51 Dominium existing tool wrapper pilot for XStack/AuditX/RepoX/TestX.
6. Apply only after review evidence proves no doctrine, product, queue, or tool
   overwrite risk.

Dominium must not receive source AIDE branch state, AIDE queue history, or
doctrine inlined into compact memory.

## 13. Eureka Upgrade Plan

Q54-Q57 should review Eureka Q32, run upgrade preflight, sync from a stable
pack, wrap existing validators and WorkUnit systems, and then plan the first
source-observation vertical slice. Product vertical-slice work should not begin
until the governance sync review is accepted.

## 14. Red-Herring / Defer List

Do not build yet:

- live Gateway/provider routing;
- Commander/UI/mobile;
- MCP/A2A;
- active CI install;
- GitHub branch protection mutation;
- release publishing;
- Git tags;
- broad root moves;
- product feature work in Eureka or Dominium;
- deletion or renaming of XStack/AuditX/RepoX/TestX;
- exact tokenizer or billing proof;
- autonomous worker execution.

## 15. Final Next Queue

The canonical next queue is in `next-queue.md`. Q35 is now complete, so the
active next AIDE-local phase is Q36.

## 16. Final Recommendation

Run Q36 Intent Compiler and Prompt Normalization v0 next. Do not execute raw
prompts directly; compile them into bounded, repo-state-first WorkUnits.
