# AIDE Operating Law

## Project Identity

- Product name: AIDE
- Expansion: Automated Integrated Development Environment
- Pronunciation: "aid"
- Canonical short namespace: `aide`

## Repository Doctrine

- AIDE is one project with one shared core and many host adapters.
- The repository is designed for long-horizon human plus agentic development.
- Governance, inventory, matrices, implementation, evaluation, and packaging are separate concerns and should not be collapsed into a single undifferentiated workstream.
- Precision, auditability, bounded scope, and deterministic verification take precedence over marketing language.

## Self-Hosting Reboot Rules

- AIDE is being rebooted in place, not restarted from scratch.
- Preserve bootstrap-era history, phase records, documents, evidence, and blocked or deferred posture.
- `.aide/profile.yaml` and declaration catalogs under `.aide/` are the canonical self-hosting Profile/Contract for the repository.
- The filesystem queue under `.aide/queue/` is the canonical source of truth for non-trivial self-hosting work.
- The Codex extension UI, chat task queue, or ad hoc prompt history is not canonical when it conflicts with `.aide/queue/`.
- AIDE must not execute raw user prompts directly; use `.aide/intake/` intent packets or filesystem queue WorkUnits for non-trivial work.
- Use `py -3 .aide/scripts/aide_lite.py intent compile --prompt "<task>"` before turning vague, repeated, destructive, target-repo, Git, release, or install prompts into implementation work.
- Non-trivial work must go through AIDE intake or a filesystem queue item with an ExecPlan, bounded scope, validation, and evidence.
- Small direct work is allowed only when `.aide/policies/bypass.yaml` permits it.
- Agents must write evidence and run proportionate validation before reporting substantial work as complete.
- Agents must stop at review gates defined in `.aide/policies/review-gates.yaml`.
- Generated downstream artifacts are outputs, not canonical contract records, unless a future reviewed policy explicitly marks them as canonical.
- The Profile is declarative; Harness commands are executable machinery and remain queue-scoped work.
- Do not build Runtime, Hosts, Commander, Mobile, Visual Studio, Xcode, VS Code, provider, or app-surface work ahead of the queue plan.

## Required Start-Of-Task Sequence

1. Inspect the repository state before editing.
2. Read the relevant governing documents for the task.
3. For any complex task, write a short plan before making edits.
4. Confirm the allowed paths and keep the change set inside them.
5. Execute the smallest coherent diff that satisfies the prompt.
6. Verify the result before concluding.

## Plan-First Rule

- Complex tasks require plan-first behavior.
- A task is complex if it touches multiple files, defines policy, changes architecture, introduces new structure, or has non-trivial verification requirements.
- A plan should identify objective, scope, dependencies, verification intent, and likely blockers.
- Do not start broad edits until that plan exists.

## Naming And Coverage Law

- Directory names must be based on compatibility technology or host contract, not version ranges, date spans, or vague eras.
- Exact support coverage belongs in metadata/manifests, inventory records, and support matrices.
- Do not encode exact version support into architectural source directory names.
- Do not rename established compatibility-technology directories merely because supported versions change.

## Support And Capability Law

- Support must be expressed through support tiers and capability levels, as defined in `governance/support-policy.md` and `governance/capability-levels.md`.
- Use support tiers `T0` through `T5` when describing maintenance posture.
- Use capability levels `L0` through `L4` when describing integration depth.
- Different hosts may top out at different capability levels.
- Do not imply uniform parity across all host families.
- Do not fabricate compatibility claims, support claims, or parity claims that have not been verified and recorded.

## Scope Control

- Keep diffs scoped to the task at hand.
- Avoid editing unrelated files.
- Do not silently expand scope because a broader change seems useful.
- If a cross-cutting fix is necessary for coherence, keep it minimal and record the reason in `IMPLEMENT.md`.
- Preserve existing user changes and fix forward.

## Verification Law

- No substantial task is complete until verification has been run.
- Verification should be proportionate to the change and explicit about what was checked.
- If runtime verification is not possible, perform the strongest honest structural verification available and record the gap.
- Never describe unrun work as verified.

## Planning And Execution Records

- `PLANS.md` is the working plan index for substantial tasks and multi-step efforts.
- `IMPLEMENT.md` is the engineering execution log for work that changed repository state.
- `DOCUMENTATION.md` is the root documentation index and maintenance guide.
- `.aide/profile.yaml` and related `.aide/` catalogs are the repo Profile/Contract source of truth; `AGENTS.md` points to that contract but does not replace it.
- `.aide/queue/` is the filesystem queue and canonical routing surface for non-trivial self-hosting work.
- ExecPlans under queue task directories are the unit of long-running autonomous work.
- When a substantial task is completed, update the relevant planning, execution, and documentation files in the same change set.

## When To Create Or Update Planning Documents

- Create or update `PLANS.md` when work spans multiple files, multiple milestones, dependencies, or blockers.
- Create or update `IMPLEMENT.md` when code, policy, or structure changes are landed.
- Create or update `DOCUMENTATION.md` when repository law, layout, or authoritative docs change.
- If a task is too small to justify a new plan entry, that should be an explicit judgment rather than an omission.

## Blockers And Deferrals

- State unresolved blockers explicitly.
- State deliberate deferrals explicitly.
- Distinguish between blocked, deferred, and completed work.
- Do not hide missing verification, missing compatibility evidence, or external constraints.

## Prohibited Behavior

- Do not fabricate compatibility, support, release readiness, or capability claims.
- Do not use vague supported or unsupported labels where the support-tier and capability-level model is required.
- Do not silently broaden product scope.
- Do not edit unrelated files to satisfy stylistic preference.
- Do not replace precise policy with speculative roadmap language.

## Commit Discipline

- Create at least one commit after each completed queued prompt when Git is available.
- Use detailed commit messages that identify prompt id, scope, key changes, verification status, and blocked or deferred notes.
- For AIDE-managed queued work, use `type(scope): summary` subjects and structured Markdown bodies with `## Summary`, `## Why`, `## Changed`, `## Validation`, `## Changelog`, `## Risks`, and `## Follow-up`.
- Run `py -3 .aide/scripts/aide_lite.py commit check --latest` or a range check before treating Q27-and-later commits as release/changelog-ready.
- Use `py -3 .aide/scripts/aide_lite.py changelog preview`, `changelog validate`, and `changelog status` for release-draft evidence; these outputs are preview-only and must not be treated as official release notes.
- Use `.aide/policies/task-resumption.yaml`, `.aide/policies/work-units.yaml`, and `.aide/policies/recovery.yaml` before asking the user about repeated, partial, duplicate, or out-of-order queue prompts.
- Prefer fix-forward history over rewriting or squashing away useful forensic context.
- If Git is not on `PATH`, use `C:\Program Files\Git\cmd\git.exe`.

## Git Branch Workflow

- Run `py -3 .aide/scripts/aide_lite.py git plan` before branch-sensitive work; use `git status` or `git detect` for additional branch context.
- Treat `main` as canonical accepted truth and `dev` as AIDE's intended shareable integration truth, not release truth.
- Normal non-trivial work should happen on a bounded task branch; direct edits on `main` are discouraged except explicitly scoped repairs.
- Do not merge, promote, prune, push, delete, or create branches without an explicit helper plan, validation evidence, and queue authorization.
- Treat `git land`, `git promote`, and `git prune` as dry-run/report-only on the live AIDE repository unless a future reviewed queue item explicitly authorizes `--apply`.
- Q30 records that local and remote `dev` are currently absent; future `dev` creation must be an explicit operator action, not an inferred repair.
- Unknown branch roles, dirty trees, missing `dev`, or stale branch state should be reported conservatively rather than fixed by ad hoc branch mutation.
- Future target sync work should import from the canonical Q31 `aide-lite-pack-v0`; do not manually copy target-local Eureka or Dominium fixes back into AIDE unless a reviewed AIDE queue phase canonicalizes them.
- Target repositories must generate their own branch detection, helper plan, task/context, review, and evidence reports after import; AIDE-generated live branch reports are not target truth.

## GitHub And CI Advisory Boundary

- Use `py -3 .aide/scripts/aide_lite.py github advisory` and `github validate` for Q35-style report-only GitHub protection and CI planning.
- Do not create `.github/workflows`, mutate GitHub branch protection, push branches, create tags, publish releases, or call GitHub APIs unless a later reviewed queue item explicitly authorizes apply behavior.
- Treat `.aide/github/**` outputs as advisory evidence, not active repository configuration.

## Repo Intelligence Boundary

- Use `py -3 .aide/scripts/aide_lite.py repo inventory`, `repo status`, `repo validate`, and `repo explain-file <path>` before judging, moving, deleting, or refactoring files.
- Treat `.aide/repo/**` outputs as deterministic evidence and conservative candidates, not deletion advice or target-repo truth.

## File Quality Boundary

- Use `py -3 .aide/scripts/aide_lite.py quality ledger`, `quality status`, `quality validate`, and `quality explain-file <path>` before turning quality concerns into refactor, docs, or test work.
- Treat `.aide/reports/file-quality-*` outputs as advisory warning evidence, not proof that files are dead, safe to delete, safe to move, or automatically fixable.

## Refactor Control Boundary

- Use `py -3 .aide/scripts/aide_lite.py refactor status`, `refactor plan`, `refactor validate`, and `refactor dry-run` before proposing structural moves, salvage, aliases, migrations, or root recycling.
- Treat `.aide/refactors/latest-*` outputs as dry-run planning evidence only. Q39 does not authorize file moves, deletes, reference rewrites, migration apply, target-repo mutation, branch mutation, or deletion approval.

## Root Recycling Boundary

- Use `py -3 .aide/scripts/aide_lite.py roots inventory`, `roots classify`, `roots plan`, `roots validate`, `roots explain-root <root>`, and `roots explain-file <path>` before proposing root cleanup, root movement, file fates, or tool absorption.
- Treat `.aide/roots/latest-*` outputs as dry-run planning evidence only. Q40 does not authorize root moves, file moves, deletes, reference rewrites, tool absorption, target-repo mutation, branch mutation, or deletion approval.
- Treat `drop_candidate` as a review candidate only, never as proof that a file is safe to delete.

## Tool Absorption Boundary

- Use `py -3 .aide/scripts/aide_lite.py tools inventory`, `tools classify`, `tools wrap-plan`, `tools validate`, `tools status`, `tools capabilities`, and `tools explain-tool <path>` before proposing to wrap, adapt, migrate, rename, replace, or retire existing repo tools.
- Treat `.aide/tools/latest-*` outputs as no-execution planning evidence only. Q41 does not authorize unknown tool execution, tool deletion, tool rename, tool migration, active wrapper execution, target-repo mutation, branch mutation, or deletion approval.
- Treat `wrap`, `adapt`, and `drop_candidate` as future review candidates only, never as proof that a tool can be executed, rewritten, renamed, migrated, or deleted.

## Move/Salvage/Alias Boundary

- Use `py -3 .aide/scripts/aide_lite.py refactor map`, `refactor validate-map`, and `refactor map-status` before proposing file moves, salvage extraction, path aliases, shims, or reference rewrites.
- Treat `.aide/refactors/current-*`, `.aide/refactors/path-aliases.*`, `.aide/refactors/reference-rewrite-plan.*`, and `.aide/refactors/migration-ledger.draft.jsonl` as candidate evidence only. Q42 does not authorize file moves, deletes, reference rewrites, alias/shim creation, target-repo mutation, branch mutation, or deletion approval.
- Treat all current maps as local source evidence; target repositories must generate their own maps after import.

## Install Planning Boundary

- Use `py -3 .aide/scripts/aide_lite.py install observe`, `install plan`, `install dry-run`, `install validate`, `install status`, and `install explain <path>` before proposing AIDE install, repair, upgrade, rollback, or uninstall work in a target repo.
- Treat `.aide/install/latest-*` outputs as no-apply planning evidence only. Q43 does not authorize install apply, file overwrites, migrations, file moves/deletes, reference rewrites, target-repo mutation, branch mutation, or source-generated state as target truth.

## Repair / Doctor Boundary

- Use `py -3 .aide/scripts/aide_lite.py repair observe`, `repair diagnose`, `repair plan`, `repair dry-run`, `repair validate`, `repair status`, `repair classes`, `repair doctor`, and `repair explain <issue-or-path>` before proposing repairs for broken, stale, partial, or inconsistent AIDE installs.
- Treat `.aide/repair/latest-*` outputs as no-apply planning evidence only. Q44 does not authorize repair apply, overwrites, deletions, migrations, file moves, reference rewrites, target-repo mutation, branch mutation, or source-state replacement.
- Treat tracked local state, secret-like paths, unsupported schemas, and source-state contamination as blockers or manual-review issues, not automatic repair work.

## Upgrade Boundary

- Use `py -3 .aide/scripts/aide_lite.py upgrade observe-current`, `upgrade observe-source`, `upgrade compare`, `upgrade plan`, `upgrade dry-run`, `upgrade validate`, `upgrade status`, `upgrade compatibility`, `upgrade conflicts`, `upgrade migrations`, and `upgrade explain <path-or-issue>` before proposing updates from one AIDE pack/version state to another.
- Treat `.aide/upgrade/latest-*` outputs as no-apply planning evidence only. Q45 does not authorize upgrade apply, overwrites, deletions, migrations, install apply, repair apply, file moves, reference rewrites, target-repo mutation, branch mutation, or source-generated state as target truth.
- Preserve target memory, queue, evidence, target golden tasks, generated target reports, manual guidance, and existing tools unless a future explicit apply phase has reviewed evidence and rollback/uninstall prerequisites.

## Rollback / Uninstall Boundary

- Use `py -3 .aide/scripts/aide_lite.py rollback observe`, `rollback plan`, `rollback dry-run`, `rollback validate`, `rollback status`, `rollback classes`, and `rollback explain <path-or-issue>` before proposing rollback or upgrade recovery work.
- Use `py -3 .aide/scripts/aide_lite.py uninstall observe`, `uninstall plan`, `uninstall dry-run`, `uninstall validate`, `uninstall status`, `uninstall classes`, and `uninstall explain <path-or-issue>` before proposing AIDE removal work.
- Treat `.aide/rollback/latest-*` and `.aide/uninstall/latest-*` outputs as no-apply planning evidence only. Q46 does not authorize rollback apply, uninstall apply, file deletion, overwrites, managed-section removal, file moves, reference rewrites, target-repo mutation, branch mutation, or source-generated state as target truth.
- Uninstall is not blanket `.aide` deletion. Preserve target memory, queue, evidence, target golden tasks, generated target state, manual guidance, existing tools, local ignored state, and unknown ownership unless a future explicit apply phase has reviewed ownership evidence and recovery requirements.

## Expected Final Report After Each Task

1. A short summary of what changed.
2. A file list.
3. The verification commands that were run and whether they passed.
4. Any unresolved issues or deliberate deferrals.

<!-- AIDE-GENERATED:BEGIN section=aide-self-hosting-summary generator=aide-harness-generated-artifacts-v0 version=q05.generated-artifacts.v0 mode=managed-section sources=.aide/profile.yaml,.aide/toolchain.lock,.aide/commands/catalog.yaml,.aide/queue/policy.yaml,.aide/queue/index.yaml,docs/reference/source-of-truth.md,docs/reference/harness-v0.md,docs/reference/generated-artifacts-v0.md fingerprint=sha256:3c125754e96bd2007d2ffd5874811c4c8b837bf146207ea1a01a7f8d275ee481 manual=outside-only -->
## Generated AIDE Contract Summary

- Canonical Profile/Contract source: `.aide/`.
- Canonical long-running work queue: `.aide/queue/`.
- Generated downstream artifacts are compiled or managed outputs, not canonical truth.
- Non-trivial work must route through AIDE intake or the filesystem queue and produce evidence.
- Current accepted foundation includes Contract/Profile v0, Harness v0, Compatibility baseline records, the AIDE-side Dominium Bridge baseline, and report-first self-hosting automation.
- Runtime, full Hosts, Gateway, providers, Commander, Mobile, app surfaces, and real Dominium Bridge implementation remain deferred until queue items authorize them.
<!-- AIDE-GENERATED:END section=aide-self-hosting-summary -->

<!-- AIDE-GENERATED:BEGIN section=aide-token-survival-adapter target=codex_agents_md generator=aide-adapter-compiler-v0 version=q24.existing-tool-adapter-compiler.v0 source_template=.aide/adapters/templates/AGENTS.md.template mode=managed_section manual=outside-only fingerprint=sha256:8f573bef168a6f16af88c7aef03c771d113a5971324cafb15f8b8bed4374c597 -->
## AIDE Existing-Tool Adapter: Codex

- Use `.aide/context/latest-task-packet.md` as the default task brief.
- Use `.aide/context/latest-context-packet.md` for compact repo refs when the
  task packet points there.
- Do not paste long chat history, full repo dumps, raw prompts, raw responses,
  secrets, provider keys, or `.aide.local/` contents.
- Prefer exact repo refs and line refs over copied file bodies.
- Before substantive work, run `py -3 .aide/scripts/aide_lite.py doctor`,
  `validate`, and `pack --task "<bounded task>"` when available.
- For quality-sensitive work, run `verify`, `review-pack`, `eval run`, and
  evidence checks before review or promotion.
- For Q27-and-later work, use structured commits and run `commit check` when
  practical.
- Inspect `task status` or `task inspect` before repeated, partial, or
  out-of-order queue work.
- Run `git plan` before branch-sensitive work; do not mutate branches without
  an explicit helper plan, validation evidence, and operator approval.
- Treat Gateway and provider surfaces as no-call/report-only unless a future
  reviewed queue phase explicitly enables live execution.
- Write evidence, preserve manual content, stop at review gates, and report
  validation honestly.
<!-- AIDE-GENERATED:END section=aide-token-survival-adapter -->
