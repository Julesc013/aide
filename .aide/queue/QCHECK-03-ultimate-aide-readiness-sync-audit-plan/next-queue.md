# Next Queue

## Immediate Prerequisite

### Q35 - GitHub Protection and CI Advisory v0

- Purpose: define report-only GitHub branch protection and CI advisory policy.
- Must produce: policies, advisory reports, validation commands, docs, golden
  tasks, export-pack sync.
- Acceptance gate: no GitHub mutation, no CI install, no branch mutation; local
  advisory commands pass.
- Non-goals: applying branch protection, creating workflows, publishing releases.

## Q36-Q38: Intent And Intelligence

### Q36 - Intent Compiler and Prompt Normalization v0

- Purpose: compile vague, broad, repeated, or wrong prompts into bounded
  WorkUnits.
- Must produce: intent policy, compiler command, normalized WorkUnit packet,
  split/no-op/block decisions, tests.
- Acceptance gate: raw prompt never executes directly.
- Non-goals: autonomous execution.

### Q37 - Repo Intelligence Index v0

- Purpose: build deterministic repo indexes for files, roots, ownership,
  dependencies, tests, docs, generated/manual status, and target tools.
- Must produce: JSON/Markdown indexes and command surface.
- Acceptance gate: no source dumps, deterministic outputs.
- Non-goals: refactor or deletion.

### Q38 - File Quality Ledger v0

- Purpose: record stale paths, orphan files, ownership gaps, docs drift,
  generated/manual boundary risks, and test coverage gaps.
- Must produce: ledger schema, reports, tests, docs.
- Acceptance gate: findings are advisory and path-specific.
- Non-goals: automatic cleanup.

## Q39-Q42: Refactor And Tool Absorption Control

### Q39 - Refactor Policy and Migration Ledger v0

- Purpose: define safe refactor proposal rules and migration ledger.
- Must produce: policy, ledger schema, dry-run report.
- Acceptance gate: no moves.
- Non-goals: broad refactor.

### Q40 - Root Inventory and Recycling Plan v0

- Purpose: classify root directories and root-recycling candidates.
- Must produce: root inventory, status taxonomy, candidate report.
- Acceptance gate: no moves/deletions.
- Non-goals: root rewrite.

### Q41 - Existing Tool Absorption Registry v0

- Purpose: register target tools such as XStack, AuditX, RepoX, TestX, Eureka
  validators, command matrices, and task catalogs.
- Must produce: absorption registry, wrapper plan, evidence mapping.
- Acceptance gate: preserve and classify tools.
- Non-goals: replacing target tools.

### Q42 - Dry-Run Move, Salvage, and Alias Planner v0

- Purpose: plan moves/salvage/aliases without applying them.
- Must produce: move map, salvage map, path aliases, rollback notes.
- Acceptance gate: dry-run only.
- Non-goals: filesystem moves.

## Q43-Q48: Install, Upgrade, Rollback, Release Drafts

### Q43 - Install Preflight and Ownership Ledger v0

- Purpose: inspect target before install/upgrade.
- Must produce: preflight schema, ownership ledger, conflict taxonomy.
- Acceptance gate: no writes to targets.
- Non-goals: installer apply.

### Q44 - Installer Observe/Plan/Dry-Run v0

- Purpose: generate target-safe install plans.
- Must produce: install plan, dry-run report, tests.
- Acceptance gate: no apply by default.
- Non-goals: broad target mutation.

### Q45 - Upgrade, Repair, and Rollback Planner v0

- Purpose: define reversible upgrade and repair plans.
- Must produce: upgrade plan, repair plan, rollback plan.
- Acceptance gate: rollback evidence exists before apply.
- Non-goals: live target apply.

### Q46 - Uninstall and State Preservation Planner v0

- Purpose: plan removal of AIDE surfaces while preserving target state.
- Must produce: uninstall plan and preserved-state report.
- Acceptance gate: no destructive default.
- Non-goals: deleting target tools.

### Q47 - Stable Pack Release Bundle Draft v0

- Purpose: assemble a reviewable pack release bundle.
- Must produce: bundle manifest, checksums, release-readiness report.
- Acceptance gate: no publishing.
- Non-goals: package publication.

### Q48 - GitHub Release Draft Integration v0

- Purpose: generate preview-only GitHub release text from changelog outputs.
- Must produce: draft text and validation.
- Acceptance gate: no GitHub API mutation.
- Non-goals: GitHub Release creation.

## Q49-Q53: Dominium Install And Absorption

### Q49 - Dominium Fresh Install Preflight

- Purpose: inspect Dominium target state, doctrine, tools, and conflicts.
- Must produce: preflight report and no-overwrite plan.
- Acceptance gate: read-only.
- Non-goals: product changes.

### Q50 - Dominium Stable Pack Upgrade Dry-Run

- Purpose: dry-run upgrade from stable pack.
- Must produce: conflict report, ownership ledger, validation plan.
- Acceptance gate: no apply.
- Non-goals: doctrine rewrite.

### Q51 - Dominium Existing Tool Wrapper Pilot

- Purpose: wrap XStack/AuditX/RepoX/TestX outputs as AIDE evidence.
- Must produce: wrapper registry and sample reports.
- Acceptance gate: no target tool deletion.
- Non-goals: extraction.

### Q52 - Dominium Root Recycling Dry-Run Pilot

- Purpose: identify root cleanup candidates without moving files.
- Must produce: root inventory and dry-run move/salvage maps.
- Acceptance gate: no moves.
- Non-goals: root rewrite.

### Q53 - Dominium Operating Baseline

- Purpose: record post-sync operating baseline and next product-safe task.
- Must produce: baseline packet and validation evidence.
- Acceptance gate: doctrine preserved.
- Non-goals: product implementation.

## Q54-Q57: Eureka Upgrade And First Bounded Work

### Q54 - Eureka Upgrade Preflight and Tool Absorption Audit

- Purpose: inspect Eureka sync state, validators, WorkUnit systems, and conflicts.
- Must produce: preflight and absorption report.
- Acceptance gate: read-only.
- Non-goals: product changes.

### Q55 - Eureka Stable Pack Upgrade Dry-Run

- Purpose: dry-run upgrade from stable pack.
- Must produce: conflict report and validation plan.
- Acceptance gate: no apply.
- Non-goals: branch mutation.

### Q56 - Eureka Existing Validator Wrapper Pilot

- Purpose: wrap architecture checks and local validators into AIDE evidence.
- Must produce: wrapper reports and tests.
- Acceptance gate: existing validators preserved.
- Non-goals: replacing validators.

### Q57 - Eureka Source Observation Vertical Slice Plan

- Purpose: select the first bounded source-observation product task.
- Must produce: WorkUnit packet and acceptance gate.
- Acceptance gate: Q32/Q54-Q56 accepted.
- Non-goals: broad product feature work.
