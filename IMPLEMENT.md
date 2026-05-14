# AIDE Implementation Log

## Purpose

`IMPLEMENT.md` is the engineering execution log for repository changes. It records what changed, why it changed, how it was verified, which risks were avoided, and what remains unresolved. It is not a changelog.

## What To Record

- the work item or prompt id
- the changed paths
- the rationale for the change
- notable design decisions and policy choices
- tradeoffs accepted
- verification that was run
- regressions or scope errors explicitly avoided
- remaining issues, blockers, or deliberate deferrals

## Entry Template

```md
## Work Item: PX

### Status

### Changed Paths

### Rationale

### Notable Design Decisions

### Tradeoffs

### Verification

### Regressions Avoided

### Remaining Issues
```

## Current Execution Log

## Work Item: Q48

Implemented for review as local-only GitHub Release draft generation from the
Q47 AIDE Lite release bundle.

Changed:

- `.aide/queue/Q48-github-release-draft-v0/**`
- `.aide/policies/github-release-draft.yaml`
- `.aide/policies/release-publication-boundary.yaml`
- `.aide/policies/release-upload-plan.yaml`
- `.aide/policies/release-checklist.yaml`
- `.aide/release/github-release-*.schema.json`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q48_github_release_draft.py`
- `.aide/evals/golden-tasks/**`
- `docs/reference/github-release-draft.md`

Q48 generates local draft Markdown/JSON, asset lists with checksums, no-upload
plans, publication checklists, publication-boundary reports, and draft
validation. It does not create tags, call GitHub APIs, create GitHub Releases,
upload assets, publish packages, mutate branches, install CI, mutate target
repos, call providers/models/network, or apply install/repair/upgrade/rollback/
uninstall actions.

The next phase is Q49 Dominium Fresh Install Preflight, because target install
readiness still needs target-local evidence.

## Work Item: Q47

### Status

Implemented for review as local-only AIDE Lite release bundle generation and
validation.

### Scope

- `.aide/queue/Q47-aide-lite-release-bundle-v0/**`
- `.aide/policies/release-bundle.yaml`
- `.aide/policies/release-artifacts.yaml`
- `.aide/policies/release-provenance.yaml`
- `.aide/policies/release-validation.yaml`
- `.aide/policies/release-versioning.yaml`
- `.aide/release/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q47_release_bundle.py`
- `.aide/evals/golden-tasks/release_*_golden/**`
- docs, latest Q48 task packet, and export-pack updates

### Rationale

Q47 turns the validated portable AIDE Lite Pack into local downloadable
artifacts before any public release draft or publication work. The bundle must
be inspectable, checksummed, extractable, and explicit about its no-publish and
no-apply boundaries before target installation or upgrade phases can use it as
a stable source.

### Notable Design Decisions

The release command surface uses Python standard-library archive, checksum, and
temporary extraction support only. Archives are built from
`.aide/export/aide-lite-pack-v0/`, not from arbitrary source paths, and release
validation rejects forbidden archive paths such as `.git/`, `.aide.local/`,
`.env`, secrets, and raw prompt or response logs.

### Tradeoffs

Q47 can generate `.zip` and `.tar.gz` archives locally, but it deliberately
does not publish them, tag a commit, upload artifacts, create a GitHub Release,
or install AIDE into a target repository. Release notes and changelog copies
remain preview-only.

### Verification

Q47 evidence records release bundle generation, archive extraction validation,
checksum verification, forbidden-path checks, targeted release tests, golden
tasks, pack-status, and broader AIDE validation.

### Regressions Avoided

No Git tag, GitHub Release, artifact upload, branch mutation, target-repo
mutation, active CI installation, install/repair/upgrade/rollback/uninstall
apply, provider/model/network call, or release publication is introduced.

### Remaining Issues

- Q47 is local bundle generation only; Q48 is needed for GitHub Release draft
  planning.
- Target repositories still need their own install, repair, upgrade, rollback,
  or uninstall preflights.
- Apply-capable install and upgrade behavior remains future-gated.

## Work Item: QFIX-05

### Status

Implemented for review as a bounded release-readiness warning reconciliation.

### Changed Paths

- `.aide/queue/QFIX-05-release-readiness-warning-reconciliation/**`
- `.aide/queue/index.yaml`
- `.aide/generated/manifest.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The broad request to make every prior task production-ready cannot safely bypass
AIDE queue law or review gates. QFIX-05 inventories the current state, fixes the
mechanical generated-manifest warning, and records the remaining release
blockers explicitly.

### Notable Design Decisions

- Preserved Q36-Q46 and QFIX-04 as `needs_review`.
- Used the deterministic Harness compiler for generated artifact refresh.
- Treated release publication, tag creation, GitHub mutation, branch mutation,
  target repo mutation, and provider/model/network calls as out of scope.

### Verification

Validation is recorded in
`.aide/queue/QFIX-05-release-readiness-warning-reconciliation/evidence/validation.md`.

### Remaining Issues

Immediate public release is still blocked by review gates and the future Q48
release-draft phase.

## Work Item: QFIX-04

### Status

Implemented for review as a bounded AIDE Lite selftest performance hotfix.

### Changed Paths

- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_golden_tasks.py`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/queue/QFIX-04-aide-lite-selftest-performance/**`
- `.aide/queue/index.yaml`

### Rationale

The broad performance request was not safe to execute as a speculative
repo-wide rewrite. Profiling identified one concrete hot path: AIDE Lite
`test`/`selftest` spent most of its time running the full golden-task catalog,
even though full catalog validation is already available through `eval run`.

### Notable Design Decisions

- Kept full `eval run` behavior intact.
- Limited selftest golden coverage to a representative smoke set.
- Reused one context compilation result for snapshot, index, and context
  assertions.
- Avoided repeated path normalization in ignore matching.

### Verification

Validation is recorded in
`.aide/queue/QFIX-04-aide-lite-selftest-performance/evidence/validation.md`.

### Remaining Issues

This is not a complete performance program. Follow-up WorkUnits should target
full golden-task data caching, inventory scan reuse, and harness subprocess
overhead.

## Work Item: Q46

### Status

Implemented for review as deterministic rollback and uninstall observe/plan/
dry-run planning with preservation-first ownership gates.

### Scope

- `.aide/queue/Q46-rollback-uninstall-model-v0/**`
- `.aide/policies/rollback.yaml`
- `.aide/policies/rollback-classes.yaml`
- `.aide/policies/rollback-safety.yaml`
- `.aide/policies/rollback-verification.yaml`
- `.aide/policies/uninstall.yaml`
- `.aide/policies/uninstall-classes.yaml`
- `.aide/policies/uninstall-safety.yaml`
- `.aide/policies/uninstall-verification.yaml`
- `.aide/rollback/**`
- `.aide/uninstall/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q46_rollback_uninstall.py`
- `.aide/evals/golden-tasks/rollback_*_golden/**`
- `.aide/evals/golden-tasks/uninstall_*_golden/**`
- docs, latest Q47 task packet, and export-pack updates

### Rationale

Q46 closes the no-apply install governance loop created by Q43-Q45. Future
target installs, repairs, and upgrades need explicit rollback and uninstall
contracts before any target mutation can be reviewed as reversible.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-apply in Q46. Rollback and uninstall read install ownership ledgers and prior
install, upgrade, or repair plans when present, but missing ownership evidence
does not become removal permission. Unknown ownership is preserved, blocked, or
sent to manual review.

### Tradeoffs

The current AIDE-source rollback and uninstall plans are conservative. They may
list many portable-file future candidates, but all operations carry
`apply_allowed: false`, deletion and managed-section removal are disabled by
default, and target-specific state is preserved.

### Verification

Q46 evidence records rollback observe/plan/dry-run/validate/status/classes/
explain commands, uninstall observe/plan/dry-run/validate/status/classes/
explain commands, targeted Q46 tests, golden tasks, pack-status, and broader
AIDE validation.

### Regressions Avoided

No rollback apply, uninstall apply, install apply, repair apply, upgrade apply,
delete, overwrite, managed-section removal, migration apply, file move,
reference rewrite, target-repo mutation, branch mutation, provider/model/network
call, release publishing, or source-generated rollback/uninstall plan export is
introduced.

### Remaining Issues

- Q46 is planning only; rollback apply, uninstall apply, and release bundle
  behavior remain future phases.
- Target repositories must generate their own rollback and uninstall plans.
- Q47 AIDE Lite Release Bundle v0 is needed before a release-shaped portable
  bundle can be reviewed.

## Work Item: Q45

### Status

Implemented for review as deterministic observe-current/observe-source/compare/
plan/dry-run upgrade planning and compatibility reporting.

### Scope

- `.aide/queue/Q45-upgrade-model-v0/**`
- `.aide/policies/upgrade.yaml`
- `.aide/policies/upgrade-compatibility.yaml`
- `.aide/policies/upgrade-preservation.yaml`
- `.aide/policies/upgrade-conflicts.yaml`
- `.aide/policies/upgrade-migrations.yaml`
- `.aide/policies/upgrade-verification.yaml`
- `.aide/upgrade/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q45_upgrade_model.py`
- `.aide/evals/golden-tasks/upgrade_*_golden/**`
- docs, latest Q46 task packet, and export-pack updates

### Rationale

Q45 turns Q43 install planning and Q44 repair diagnosis into upgrade planning
infrastructure. Future target upgrades can compare current installed AIDE state
to a source pack, preserve target-specific memory and evidence, classify
compatibility, and dry-run candidate updates before any target file is changed.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-apply in Q45. It reads export-pack manifests and payloads when present,
preserves target queue, memory, evidence, generated target state, target golden
tasks, manual guidance, and existing tools, and writes generated planning
outputs under `.aide/upgrade/`.

### Tradeoffs

Compatibility classification is structural and conservative. When evidence is
uncertain, the plan uses warning, preserve, skip, manual review, or future
migration language rather than treating a difference as safe to apply.

### Verification

Q45 evidence records upgrade observe-current/observe-source/compare/plan/
dry-run/validate/status/compatibility/conflicts/migrations/explain commands,
targeted Q45 tests, golden tasks, pack-status, and broader AIDE validation.

### Regressions Avoided

No upgrade apply, install apply, repair apply, overwrite, delete, migration
apply, file move, reference rewrite, target-repo mutation, branch mutation,
provider/model/network call, release publishing, or source-generated upgrade
plan export is introduced.

### Remaining Issues

- Q45 is planning only; upgrade apply, rollback, uninstall, and release bundle
  behavior remain future phases.
- Target repositories must generate their own upgrade observations and plans.
- Q46 Rollback / Uninstall Model v0 is needed before future apply phases can
  rely on reversible target mutation contracts.

## Work Item: Q44

### Status

Implemented for review as deterministic observe/diagnose/plan/dry-run repair
planning and advisory doctor reporting.

### Scope

- `.aide/queue/Q44-repair-doctor-model-v0/**`
- `.aide/policies/repair.yaml`
- `.aide/policies/repair-classes.yaml`
- `.aide/policies/repair-safety.yaml`
- `.aide/policies/repair-detection.yaml`
- `.aide/policies/repair-verification.yaml`
- `.aide/policies/doctor.yaml`
- `.aide/repair/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q44_repair_doctor.py`
- `.aide/evals/golden-tasks/repair_*_golden/**`
- docs, latest Q45 task packet, and export-pack updates

### Rationale

Q44 turns Q43 install planning, conflict reporting, preservation rules, and
pack references into repair diagnosis infrastructure. Future target repairs can
be observed, classified, planned, dry-run, and reviewed before any target file
is changed.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-apply in Q44. It reads install artifacts and pack files when present, writes
generated planning outputs under `.aide/repair/`, preserves target memory,
queue, evidence, docs, tools, and manual content, and treats local state,
secrets, unsupported schemas, and source-state contamination as blockers or
manual-review issues rather than automatic repair work.

### Verification

Q44 evidence records repair observe/diagnose/plan/dry-run/validate/status/
classes/doctor/explain commands, targeted unit tests, golden tasks, AIDE Lite
validation, export-pack regeneration, pack-status, diff checks, core unittest
suites where available, and secret scan results.

### Remaining Issues

- Q44 is planning only; repair apply, upgrade, rollback, uninstall, and install
  apply behavior remain future work.
- Repair classification is heuristic and must be reviewed before target
  mutation.
- Target repositories must generate their own `.aide/repair/latest-*` outputs;
  AIDE source-generated repair outputs are not portable target truth.
- Q45 Upgrade Model v0 is needed before upgrade decisions can use repair
  diagnosis and install preservation evidence.

## Work Item: Q43

### Status

Implemented for review as deterministic observe/plan/dry-run install planning.

### Scope

- `.aide/queue/Q43-install-plan-model-v0/**`
- `.aide/policies/install.yaml`
- `.aide/policies/install-preservation.yaml`
- `.aide/policies/install-ownership.yaml`
- `.aide/policies/install-conflicts.yaml`
- `.aide/policies/install-migrations.yaml`
- `.aide/policies/install-verification.yaml`
- `.aide/install/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q43_install_plan.py`
- `.aide/evals/golden-tasks/install_*_golden/**`
- docs, command catalog, latest Q44 task packet, and export-pack updates

### Rationale

Q43 turns Q37-Q42 repo, quality, refactor, root, tool, and map evidence into
install planning infrastructure. Future target installs can be observed,
planned, dry-run, reviewed, and checked for preservation, ownership, conflicts,
mandatory migration candidates, and verification before any target file is
changed.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-apply in Q43. It reads the current portable pack when present, writes
generated planning outputs under `.aide/install/`, preserves target memory,
queue, evidence, docs, tools, and manual content, and treats source-generated
state as evidence to regenerate locally rather than target truth.

### Verification

Q43 evidence records install observe/plan/dry-run/validate/status/ownership/
conflicts/explain commands, targeted unit tests, golden tasks, AIDE Lite
validation, export-pack regeneration, pack-status, diff checks, core unittest
suites where available, and secret scan results.

### Remaining Issues

- Q43 is planning only; install apply, repair, upgrade, rollback, and uninstall
  behavior remain future work.
- Conflict and ownership classification is heuristic and must be reviewed before
  target mutation.
- Target repositories must generate their own `.aide/install/latest-*` outputs;
  AIDE source-generated install outputs are not portable target truth.
- Q44 Repair / Doctor Model v0 is needed before repair decisions can consume
  Q43 conflict and preservation evidence.

## Work Item: Q42

### Status

Implemented for review as deterministic no-apply map and alias planning.

### Scope

- `.aide/queue/Q42-move-map-salvage-map-path-alias-v0/**`
- `.aide/policies/move-map.yaml`
- `.aide/policies/salvage-map.yaml`
- `.aide/policies/path-aliases.yaml`
- `.aide/policies/reference-rewrite.yaml`
- `.aide/policies/migration-ledger.yaml`
- `.aide/refactors/*map*.schema.json`
- `.aide/refactors/path-alias*.schema.json`
- `.aide/refactors/reference-rewrite*.schema.json`
- `.aide/refactors/migration-ledger*.schema.json`
- `.aide/refactors/current-*`, `path-aliases.*`, `reference-rewrite-plan.*`, `migration-ledger.draft.jsonl`, and `map-validation-report.*`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q42_move_map_aliases.py`
- `.aide/evals/golden-tasks/*map*_golden/**`
- `.aide/evals/golden-tasks/path_alias_policy_golden/**`
- `.aide/evals/golden-tasks/reference_rewrite_plan_golden/**`
- `.aide/evals/golden-tasks/migration_ledger_policy_golden/**`
- docs, command catalog, latest Q43 task packet, and export-pack updates

### Rationale

Q42 turns Q37 repo intelligence, Q38 quality evidence, Q39 refactor controls,
Q40 root evidence, and Q41 tool preservation plans into map-level planning
evidence. Future install, repair, upgrade, rollback, root recycling, and tool
absorption phases can cite candidate path mappings before any file move,
salvage extraction, alias, shim, or reference rewrite is considered.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
candidate-only in Q42. It writes current move/salvage/alias/rewrite/ledger
draft artifacts under `.aide/refactors/`, but every current entry remains
`apply_allowed: false`. It never moves files, deletes files, rewrites
references, creates aliases or shims, applies maps, mutates branches, mutates
target repos, calls providers/models/network services, or treats
`drop_candidate` as deletion approval.

### Verification

Final Q42 evidence records Harness validation, AIDE Lite validation, repo,
quality, refactor, roots, tools, and map commands, Q42 unit tests, golden tasks,
export-pack regeneration, pack-status, core unittest suites, diff checks, and
secret scan results.

### Remaining Issues

- Q42 is candidate planning only; no concrete Dominium, Eureka, or AIDE root
  migration is implemented.
- Current move-map generation is intentionally sparse until a future reviewed
  task selects a concrete root or target path plan.
- No alias, shim, salvage extraction, reference rewrite, install, repair,
  upgrade, rollback, or apply behavior exists yet.
- Target repositories must generate their own maps after import; source
  `.aide/refactors/current-*` outputs are not portable target truth.

## Work Item: Q41

### Status

Implemented for review as deterministic no-execution existing-tool absorption
planning.

### Scope

- `.aide/queue/Q41-existing-tool-absorption-v0/**`
- `.aide/policies/tool-absorption.yaml`
- `.aide/policies/tool-inventory.yaml`
- `.aide/policies/tool-fates.yaml`
- `.aide/policies/tool-wrapping.yaml`
- `.aide/policies/tool-risk.yaml`
- `.aide/policies/tool-capabilities.yaml`
- `.aide/tools/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q41_tool_absorption.py`
- `.aide/evals/golden-tasks/tool_*_golden/**`
- `.aide/evals/golden-tasks/tools_no_execution_golden/**`
- docs, command catalog, latest Q42 task packet, and export-pack updates

### Rationale

Q41 turns Q37 repo intelligence, Q38 quality evidence, Q39 refactor controls,
and Q40 root evidence into tool-level planning evidence. Future target repos
can discover XStack, AuditX, RepoX, TestX, project validators, scripts,
command catalogs, and CI wrappers before AIDE decides whether to keep, wrap,
adapt, extract, convert, shim, or leave them for review.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-execution in Q41. It writes `.aide/tools/` inventory, classification, wrap
plan, adapter map, and risk outputs. It never executes unknown tools, deletes
tools, renames tools, migrates tools, actively wraps tools, mutates branches,
mutates target repos, calls providers/models/network services, or treats
`drop_candidate` as deletion approval.

### Verification

Final Q41 evidence records Harness validation, AIDE Lite validation, repo,
quality, refactor, roots, and tools commands, Q41 unit tests, golden tasks,
export-pack regeneration, pack-status, core unittest suites, diff checks, and
secret scan results.

### Remaining Issues

- Q41 is advisory planning only; no concrete Dominium XStack/AuditX/RepoX/TestX
  or Eureka validator absorption is implemented.
- No active wrappers, current move maps, salvage maps, path aliases, install,
  upgrade, rollback, or apply behavior exists yet.
- Tool capabilities and risks are deterministic heuristics, not semantic proof.
- Target repositories must generate their own tool inventories after import;
  source-generated `.aide/tools/latest-*` outputs are not portable target truth.

## Work Item: Q40

### Status

Implemented for review as deterministic no-apply root recycling planning.

### Scope

- `.aide/queue/Q40-root-recycling-framework-v0/**`
- `.aide/policies/root-recycling.yaml`
- `.aide/policies/root-inventory.yaml`
- `.aide/policies/root-fates.yaml`
- `.aide/policies/root-exceptions.yaml`
- `.aide/policies/root-risk.yaml`
- `.aide/refactors/root-*.schema.json`
- `.aide/roots/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q40_root_recycling.py`
- `.aide/evals/golden-tasks/root_*_golden/**`
- `.aide/evals/golden-tasks/roots_no_apply_golden/**`
- docs, command catalog, latest Q41 task packet, and export-pack updates

### Rationale

Q40 turns Q37 repo intelligence, Q38 quality evidence, and Q39 refactor
controls into root-level planning evidence. Future root cleanup can now start
with deterministic root inventory, root status, risk, exception, and per-file
fate candidates instead of broad folder movement or deletion prompts.

### Notable Design Decisions

The framework is deterministic, repo-local, Python standard-library only, and
no-apply in Q40. It writes `.aide/roots/` inventory, classification, plan,
exception, and risk outputs. It never moves roots, deletes files, rewrites
references, applies maps, absorbs tools, mutates branches, mutates target
repos, calls providers/models/network services, or treats `drop_candidate` as
deletion approval.

### Verification

Final Q40 evidence records Harness validation, AIDE Lite validation, repo,
quality, refactor, and roots commands, Q40 unit tests, golden tasks,
export-pack regeneration, pack-status, core unittest suites, diff checks, and
secret scan results.

### Remaining Issues

- Q40 is dry-run planning only; existing tool absorption starts in Q41.
- No real current move map, salvage map, path alias, tool absorption, install,
  upgrade, rollback, or apply behavior exists yet.
- Root risks and file fates are deterministic heuristics, not semantic proof.
- Target repositories must generate their own root inventories after import;
  source-generated `.aide/roots/latest-*` outputs are not portable target truth.

## Work Item: Q39

### Status

Implemented for review as deterministic no-apply refactor planning.

### Scope

- `.aide/queue/Q39-refactor-control-plane-v0/**`
- `.aide/policies/refactor.yaml`
- `.aide/policies/migration.yaml`
- `.aide/policies/refactor-safety.yaml`
- `.aide/policies/refactor-evidence.yaml`
- `.aide/policies/refactor-application.yaml`
- `.aide/refactors/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q39_refactor_control.py`
- `.aide/evals/golden-tasks/*refactor*_golden/**`
- `.aide/evals/golden-tasks/*migration*_golden/**`
- docs, command catalog, latest Q40 task packet, and export-pack updates

### Rationale

Q39 turns Q37 repo intelligence and Q38 quality evidence into a governed
planning substrate for future structural change. Refactors can now be expressed
as dry-run plans with operations, risks, validation, evidence, rollback notes,
move maps, salvage maps, path aliases, and migration-ledger records before any
future apply phase is considered.

### Notable Design Decisions

The refactor control plane is deterministic, repo-local, Python
standard-library only, and no-apply in Q39. It writes `.aide/refactors/`
readiness/example artifacts and schema records. It never moves, deletes,
rewrites references, applies migrations, mutates branches, mutates target
repos, calls providers/models/network services, or treats `drop_candidate` as
deletion approval.

### Verification

Final Q39 evidence records Harness validation, AIDE Lite validation, repo and
quality prerequisite commands, refactor commands, Q39 unit tests, golden tasks,
export-pack regeneration, pack-status, core unittest suites, diff checks, and
secret scan results.

### Remaining Issues

- Q39 is dry-run planning only; concrete root recycling starts in Q40.
- No real current move map, salvage map, path alias, tool absorption, install,
  upgrade, rollback, or apply behavior exists yet.
- Target repositories must generate their own refactor readiness after import;
  source-generated `.aide/refactors/latest-*` outputs are not portable target
  truth.

## Work Item: Q38

### Status

Implemented for review as deterministic file quality measurement.

### Scope

- `.aide/queue/Q38-file-quality-ledger-v0/**`
- `.aide/policies/file-quality.yaml`
- `.aide/policies/docs-consistency.yaml`
- `.aide/policies/module-quality.yaml`
- `.aide/policies/reuse-modularity.yaml`
- `.aide/quality/**`
- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`
- `.aide/reports/module-quality-report.md`
- `.aide/reports/docs-consistency-report.md`
- `.aide/reports/test-coverage-map.md`
- `.aide/reports/reuse-modularity-report.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q38_file_quality.py`
- `.aide/evals/golden-tasks/*quality*_golden/**`
- docs, command catalog, latest Q39 task packet, and export-pack updates

### Rationale

Q38 turns Q37 repo intelligence into advisory quality evidence so future
WorkUnits can target small, bounded ownership, documentation, test, stale-link,
generated-boundary, module, and reuse issues instead of broad cleanup prompts.

### Notable Design Decisions

The ledger is deterministic, repo-local, Python standard-library only, and
advisory-only. It writes `.aide/reports/` quality JSON/Markdown outputs and
uses warning/candidate language. It never moves, deletes, refactors, migrates,
calls providers/models/network services, mutates target repos, or auto-fixes
source, docs, or tests.

### Verification

Final Q38 evidence records Harness validation, AIDE Lite validation, repo and
quality commands, Q38 unit tests, golden tasks, export-pack regeneration,
pack-status, core unittest suites, diff checks, and secret scan results.

### Remaining Issues

- Quality records are deterministic heuristics, not semantic quality proof.
- Warning counts are advisory and require future WorkUnits or human review.
- Orphan and reuse candidates are not deletion candidates.
- Target repositories must generate their own quality ledgers after import;
  source-generated `.aide/reports/file-quality-*` outputs are not portable
  target truth.

## Work Item: Q37

### Status

Implemented for review as deterministic repo intelligence indexing.

### Scope

- `.aide/queue/Q37-repo-intelligence-index-v0/**`
- `.aide/policies/repo-intelligence.yaml`
- `.aide/policies/file-classification.yaml`
- `.aide/policies/ownership-map.yaml`
- `.aide/policies/dependency-map.yaml`
- `.aide/policies/test-map.yaml`
- `.aide/policies/doc-link-map.yaml`
- `.aide/repo/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q37_repo_intelligence.py`
- `.aide/evals/golden-tasks/repo_*_golden/**`
- docs, command catalog, latest Q38 task packet, and export-pack updates

### Rationale

Q37 gives future WorkUnits a deterministic repo-state substrate so they do not
rediscover the file tree through long prompts or chat memory. The generated
indexes classify tracked files, owners, references, tests, docs, generated
artifacts, and conservative orphan candidates before later quality or refactor
phases act.

### Notable Design Decisions

The indexer is deterministic, repo-local, Python standard-library only, and
index-only. It reads git-tracked files when available, falls back to a bounded
filesystem walk, excludes `.git` and `.aide.local/`, computes hashes and sizes,
and writes `.aide/repo` JSON/Markdown outputs. It never moves, deletes,
refactors, migrates, calls providers/models/network services, mutates target
repos, or treats orphan candidates as deletion advice.

### Verification

Final Q37 evidence records Harness validation, AIDE Lite validation, repo
commands, Q37 unit tests, golden tasks, export-pack regeneration, pack-status,
core unittest suites, diff checks, and secret scan results.

### Remaining Issues

- Classification, dependency, test, and doc-link maps are heuristic and
  conservative.
- Unknown files and orphan candidates require Q38/Q39 follow-up before any
  quality judgment or refactor action.
- Target repositories must generate their own repo intelligence after import;
  source-generated `.aide/repo/*.json` outputs are not portable target truth.

## Work Item: Q36

### Status

Implemented for review as deterministic intent compilation and prompt
normalization.

### Scope

- `.aide/queue/Q36-intent-compiler-prompt-normalization-v0/**`
- `.aide/policies/intent.yaml`
- `.aide/policies/workunit-sizing.yaml`
- `.aide/policies/task-classes.yaml`
- `.aide/policies/risk-classes.yaml`
- `.aide/policies/prompt-normalization.yaml`
- `.aide/intake/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q36_intent_compiler.py`
- `.aide/evals/golden-tasks/intent_*_golden/**`
- `.aide/evals/golden-tasks/workunit_sizing_policy_golden/**`
- docs, command catalog, latest Q37 task packet, and export-pack updates

### Rationale

Q36 closes the raw-prompt execution gap left after Q27-Q35 governance work.
Raw prompts such as `next`, `fix everything`, `clean up the repo`, destructive
delete requests, Git promotion requests, release requests, and target install
requests now compile into reviewable intent packets and WorkUnit drafts before
any implementation work can begin.

### Notable Design Decisions

The compiler is deterministic, repo-local, Python standard-library only, and
compile-only. It reads repo policy, queue/latest-task state, and local branch
state; stores a prompt hash plus bounded excerpt; writes latest intent packet
and WorkUnit draft artifacts; and never calls providers, models, outbound
network services, GitHub APIs, Gateway forwarding, target repos, or branch
mutation commands.

### Verification

Final Q36 evidence records Harness validation, AIDE Lite validation, targeted
intent prompts, Q36 unit tests, golden tasks, export-pack regeneration,
pack-status, core unittest suites, diff checks, and secret scan results.

### Remaining Issues

- Classification confidence is heuristic and intentionally conservative.
- Q37 should add a Repo Intelligence Index so future intent packets can cite
  richer repo-local ownership and quality data.
- Q36 does not execute compiled WorkUnits, mutate targets, publish releases,
  apply GitHub/CI settings, or run provider/model/network calls.

## Work Item: Q35

### Status

Implemented as report-only GitHub protection and CI advisory tooling.

### Scope

- `.aide/queue/Q35-github-protection-ci-advisory-v0/**`
- `.aide/policies/github-protection.yaml`
- `.aide/policies/ci-gates.yaml`
- `.aide/policies/branch-protection.yaml`
- `.aide/github/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q35_github_advisory.py`
- `.aide/evals/golden-tasks/github_*_golden/**`
- `docs/reference/github-protection-ci-advisory.md`
- export-pack, command catalog, queue index, and compact docs updates

### Rationale

QCHECK-03 found Q35 missing, which left the GitHub command family unavailable
and kept Q36 planning conditional. Q35 closes that AIDE-local blocker by adding
advisory policies, generated reports, commands, tests, and export-pack support.

### Notable Design Decisions

The Q35 command family is deliberately report-only. It writes `.aide/github`
advisory artifacts but does not call GitHub APIs, create `.github/workflows`,
activate CI, mutate branches, push, create tags, publish releases, or call
providers/models/network.

### Verification

The final Q35 evidence records the full command set. Required gates include
Harness validate/doctor/self-check, AIDE Lite validate/test/selftest/eval,
GitHub advisory commands, commit check, changelog validate, Git policy,
export-pack, pack-status, core unittest suites, and secret scan.

### Remaining Issues

Active GitHub protection and CI installation remain future apply-capable work
that requires dry-run evidence, rollback, operator approval, and review gates.

## Work Item: QFIX-03

### Status

Implemented as warning and review reconciliation; accepted with notes in the
queue state.

### Scope

- `.aide/queue/**/status.yaml`
- `.aide/queue/**/task.yaml`
- `.aide/queue/index.yaml`
- `.aide/generated/manifest.yaml`
- `.aide/scripts/aide_lite.py`
- `.aide/policies/changelog.yaml`
- `.aide/policies/token-budget.yaml`
- `.aide/reports/token-ledger.jsonl`
- `.aide/reports/token-savings-summary.md`
- `.aide/profile.yaml`
- `.aide/memory/**`
- `core/harness/**`
- `core/compat/**`
- root documentation summaries

### Implementation Notes

QFIX-03 resolved the stale generated-manifest warning, reconciled completed
review-gated queue items from task-local evidence, and converted Q25-Q31/Q34
from pending review to `passed_with_notes`. The review reconciliation explicitly
does not claim product readiness, live provider/model calls, release readiness,
target-repo mutation, live branch mutation, or generated outputs as canonical
truth.

Q34 changelog preview now treats malformed or legacy history as reportable
review findings rather than a command-level warning. The malformed commit report
and JSON counts remain in place so old history is not hidden.

Harness doctor/self-check guidance reported the reconciled queue state and
pointed to Q35 at the time of QFIX-03, rather than stale Q25/Q26/Q27 review guidance. The token ledger
now distinguishes hard budget warnings from near-budget watchlist entries and
uses an explicit eval-report budget for the 30-task golden report.

### Verification Notes

QFIX-03 reruns Harness validation, AIDE Lite validation/test/selftest/eval,
commit checks, changelog preview/validate/status, pack export/status, and core
unit test suites. Final Harness and AIDE Lite validation report PASS with no
WARN/FAIL checks. Detailed results are recorded in
`.aide/queue/QFIX-03-warning-review-reconciliation/evidence/validation.md`.

### Regressions Avoided

- No Git history rewrite.
- No provider/model/network calls.
- No release publishing, tags, GitHub Releases, or GitHub API mutation.
- No target-repo mutation.

### Follow-Up

- Q35 has since been implemented as report-only advisory work; Q36 is the next AIDE-local phase.

## Work Item: Q34

### Status

Implemented, awaiting review.

### Scope

- `.aide/policies/changelog.yaml`
- `.aide/changelog/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q34_changelog_release.py`
- `.aide/evals/golden-tasks/**`
- `.aide/queue/Q34-changelog-release-notes-generator-v0/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/changelog-preview.md`

### Implementation Notes

Q34 turns Q27 structured commit bodies into deterministic preview artifacts:
`CHANGELOG.preview.md`, `RELEASE_NOTES.preview.md`, matching JSON files,
`malformed-commits.md`, and `latest-changelog-report.md`. The parser reads
Conventional Commit subjects, structured Markdown sections, changelog category
bullets, AIDE trailers, legacy semi-structured commits, merge commits, and
breaking-change markers. Malformed or legacy commits warn and remain visible;
history is not rewritten.

The command surface is preview-only: `changelog preview` writes drafts,
`changelog validate` checks policy/templates/output shape, and
`changelog status` summarizes the latest preview. No tags, GitHub Releases,
release publishing, branch mutation, provider/model calls, or network calls
are introduced.

### Verification Notes

- Q34 targeted tests cover subject parsing, structured section extraction,
  trailer parsing, category bullets, legacy/malformed commits, merge commits,
  fixture Git history preview generation, JSON shape, and preview-only text.
- Q34 golden tasks cover changelog preview, release-note preview, malformed
  commit reporting, and JSON preview shape.
- Final validation is recorded under Q34 evidence.

### Regressions Avoided

- No official `CHANGELOG.md` promotion, release publishing, tag creation,
  GitHub Release creation, branch mutation, provider/model call, network call,
  or history rewrite.
- Export pack support includes changelog policy/config/templates but excludes
  source-generated preview outputs as target truth.

### Follow-Up

- Q35 should add GitHub protection and CI advisory policy without applying
  GitHub settings or publishing releases.

## Work Item: Q31

### Status

Implemented, awaiting review.

### Scope

- `.aide/policies/export-import.yaml`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q31_export_pack_governance.py`
- `.aide/evals/golden-tasks/**`
- `.aide/queue/Q31-export-pack-sync-git-commit-workflow/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/cross-repo-pack-export-import.md`

### Implementation Notes

Q31 makes the portable AIDE Lite Pack carry the generic governance introduced
by Q27 through Q30: structured commit policy, hook/template support,
changelog preview, task resumption, WorkUnit and recovery policy, branch role
policy, promotion/sync/prune policy, project workflow profiles, and dry-run
Git helper policy. The export boundary stays target-safe: AIDE queue history,
generated context and reports, AIDE-specific branch policy, workflow detection
outputs, latest helper plans, changelog previews, local state, secrets, raw
prompts, and raw responses remain excluded.

Safe import keeps hook installation opt-in. Imported target repos receive the
hook template under `.aide/hooks/commit-msg`, but `.git/hooks/` is not written.
Target repos must run their own `git detect`, `git plan`, snapshot, index, and
pack commands after import so target state is generated locally.

### Verification Notes

- Q31 targeted tests cover manifest inclusion, source-state exclusion, safe
  fixture import, hook non-installation, commit check pass/fail behavior, and
  imported Git policy/detect/plan commands.
- AIDE Lite Q31 golden tasks cover pack inclusion/exclusion and fixture import
  governance command behavior.
- Final validation is recorded under Q31 evidence.

### Regressions Avoided

- No Eureka, Dominium, external repo, GitHub, branch, provider, model, or
  network mutation.
- No exported AIDE-specific live branch detection or helper-plan state.
- No automatic hook installation in imported target repositories.

### Follow-Up

- Q32 should sync Eureka from the canonical Q31 pack and regenerate
  Eureka-local reports.
- Q33 should sync Dominium after Q32 evidence is available.

## Work Item: Q30

### Status

Implemented, awaiting review.

### Scope

- `.aide/git/aide-branch-policy.yaml`
- `.aide/git/aide-dev-main-plan.json`
- `.aide/git/aide-dev-main-plan.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q30_aide_dev_main_policy.py`
- `.aide/evals/golden-tasks/**`
- `.aide/queue/Q30-aide-dev-main-policy-sync/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/aide-dev-main-workflow.md`

### Implementation Notes

Q30 records the AIDE repository's own branch policy on top of the generic Q28
roles and Q29 helpers. `main` is canonical accepted truth. `dev` is the intended
shareable integration branch and is explicitly not canonical release truth.
Bounded work lands to `dev`; `dev` promotes to `main` only through review,
validation, commit, changelog, pack, and secret-scan gates.

Current local evidence shows `main` exists locally and as `origin/main`, while
`dev` is absent locally and remotely. Q30 therefore generates a future explicit
operator plan for creating and pushing `dev`, but does not run those commands.

### Verification Notes

- Q30 targeted tests cover policy parsing, main/dev role validation, no-live-
  mutation posture, missing-dev planning, existing-dev classification,
  promotion-gate anchors, and Q30 golden tasks.
- AIDE Lite Git policy, detect, status, and plan commands now include the
  AIDE-specific branch policy and generated dev/main plan artifacts.
- Final validation is recorded under Q30 evidence.

### Regressions Avoided

- No live AIDE branch creation, deletion, merge, push, prune, or promotion.
- No GitHub API calls, CI activation, release publishing, provider/model calls,
  or outbound network behavior.
- AIDE-specific live branch detection artifacts are not exported as target repo
  truth.

### Follow-Up

- Q31 should export and synchronize the generic Git/commit workflow support
  without treating AIDE's live dev/main plan as target-repo truth.
- Q35 or later should add GitHub protection and CI advisory/application layers.

## Work Item: Q29

### Status

Implemented, awaiting review.

### Scope

- `.aide/git/helper-policy.yaml`
- `.aide/git/helper-commands.md`
- `.aide/git/latest-helper-plan.json`
- `.aide/git/latest-helper-plan.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q29_git_helper.py`
- `.aide/evals/golden-tasks/**`
- `.aide/queue/Q29-merge-land-promote-helper-v0/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/git-helper-workflow.md`

### Implementation Notes

Q29 adds dry-run-first Git helper plans for sync, land, promote, and prune
actions. Live AIDE branch mutation remains out of scope: Q29 does not create
`dev`, merge into `main`, push remotes, delete live branches, or run GitHub
mutation. The mutating paths are implemented behind explicit `--apply` and
tested only inside temporary Git fixture repositories with fixture-local Git
user/email configuration.

The helper safety model records repo root, current branch, dirty state,
local/remote branches, upstream status, branch roles, protected roles, policy
readiness, ancestor containment, ahead/behind state where available, and
unpushed protected branches where feasible. Unknown or dirty states block
land/promote mutation. Prune eligibility requires ancestor containment and
never includes canonical, integration, release, or deploy roles.

### Verification Notes

- Q29 targeted fixture tests cover task-to-dev land, dev-to-main promote,
  contained branch prune, unmerged prune refusal, protected branch refusal,
  dirty-tree blocks, unknown-role blocks, and no remote push execution.
- Q29 golden tasks cover helper policy anchors, land/promote plan docs, prune
  guards, and live-repo no-mutation defaults.
- Final validation is recorded under Q29 evidence.

### Regressions Avoided

- No live AIDE branch creation, deletion, merge, push, prune, or promotion.
- No force-push support.
- No GitHub API calls, CI activation, release publishing, provider/model calls,
  or outbound network behavior.

### Follow-Up

- Q30 should decide and apply the AIDE-specific `dev`/`main` policy posture if
  appropriate.
- Q35 or later should add GitHub protection and CI advisory/application layers.

## Work Item: Q28

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/policies/git-workflow.yaml`
- `.aide/policies/branch-roles.yaml`
- `.aide/policies/promotion-rules.yaml`
- `.aide/policies/sync-policy.yaml`
- `.aide/policies/prune-policy.yaml`
- `.aide/git/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q28_git_workflow.py`
- `.aide/evals/golden-tasks/**`
- `.aide/queue/Q28-git-workflow-policy-v0/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/git-workflow-policy.md`
- `docs/reference/branch-roles.md`
- `docs/reference/promotion-policy.md`

### Rationale

Q28 makes branch state understandable before branch automation exists. It reduces
future prompt and review cost by giving agents a deterministic way to identify
`main` as canonical truth, `dev` as integration truth, task/review/release/hotfix
roles, and the policy gates that later helpers must enforce.

### Notable Design Decisions

- Detection is local and report-only; it does not fetch, merge, push, prune,
  delete, create branches, or call GitHub.
- `dev` is useful as shareable integration truth but is not canonical release
  truth.
- Unknown roles and dirty trees produce conservative recommendations.
- Pruning is policy-only and requires future ancestor-containment proof.

### Tradeoffs

- Local detection cannot prove GitHub branch protection or remote freshness.
- Full merge/land/promote behavior is deferred to Q29 so policy can be reviewed
  before mutation helpers exist.

### Verification

- Q28 targeted tests and golden tasks pass.
- Final validation is recorded under Q28 evidence.

### Regressions Avoided

- No live branch creation, deletion, merge, push, prune, fetch, or GitHub API
  mutation.
- No provider/model calls, network calls, CI creation, release publishing, or
  product runtime change.

### Remaining Issues

- Q29 must implement safe helper plans and fixture-only mutation tests.
- Q35 or later must handle GitHub branch protection and CI advisory/application.

## Work Item: Q27

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/policies/commit-messages.yaml`
- `.aide/policies/task-resumption.yaml`
- `.aide/policies/work-units.yaml`
- `.aide/policies/recovery.yaml`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q27_commit_recovery.py`
- `.aide/evals/golden-tasks/**`
- `.aide/hooks/commit-msg`
- `.aide/git/commit-template.md`
- `.aide/changelog/**`
- `.aide/queue/Q27-commit-discipline-workunit-recovery-v0/**`
- `.aide/export/aide-lite-pack-v0/**`
- `docs/reference/commit-discipline.md`
- `docs/reference/workunit-idempotency.md`
- `docs/reference/changelog-preview.md`

### Rationale

Q27 makes commits and queue tasks recoverable from repository state. It reduces
future token cost by allowing agents to validate commit bodies, preview
changelog entries, detect no-op duplicate tasks, and resume partial work without
replaying long prompt history.

### Notable Design Decisions

- Existing old commits are reported as malformed instead of rewritten.
- The commit hook is opt-in and installed only by explicit command.
- Task recovery is report-first; broad fixes still need queue authorization.
- Changelog preview is deterministic and non-publishing.

### Tradeoffs

- The changelog classifier is deliberately structural, not semantic.
- Task recovery detects queue/evidence state but does not perform product work.

### Verification

- Q27 targeted tests and golden tasks pass.
- Full final validation is recorded under Q27 evidence.

### Regressions Avoided

- No `.git/hooks` writes.
- No branch mutation, remote push, provider/model call, network call, CI, release publishing, or product runtime change.

### Remaining Issues

- CI enforcement and branch workflow policy are deferred to later Q28+ phases.
- Pre-Q27 history may remain malformed under the new checker.

## Work Item: P00

### Status

Completed

### Changed Paths

- `README.md`
- `AGENTS.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `governance/vision.md`
- `governance/support-policy.md`
- `governance/naming-policy.md`
- `governance/capability-levels.md`
- `governance/release-policy.md`

### Rationale

Replace the bootstrap placeholders with durable repository law for AIDE before any product features, host adapters, or scaffolding are introduced.

### Notable Design Decisions

- Defined AIDE as one project with one shared core and many host adapters.
- Centralized support posture in support tiers `T0` through `T5`.
- Centralized integration depth in capability levels `L0` through `L4`.
- Separated directory naming law from exact version coverage rules.
- Kept the phase release-gated so implementation work follows governance, inventory, and harness setup.

### Tradeoffs

- The documents favor durable policy over exhaustive examples.
- Future inventory and matrix details are referenced but intentionally not created in this prompt.

### Verification

- Verified file existence for all required deliverables:
  - `README.md`
  - `AGENTS.md`
  - `PLANS.md`
  - `IMPLEMENT.md`
  - `DOCUMENTATION.md`
  - `governance/vision.md`
  - `governance/support-policy.md`
  - `governance/naming-policy.md`
  - `governance/capability-levels.md`
  - `governance/release-policy.md`
- Ran `rg` checks across the deliverables for required conceptual anchors:
  - `AIDE`
  - `Automated Integrated Development Environment`
  - `one shared core`
  - `many host adapters`
  - `compatibility technology`
  - `version ranges`
  - `support tiers`
  - `capability levels`
  - `T0`
  - `T5`
  - `L0`
  - `L4`
- Verified the repository worktree shape with `git status --short`.

### Regressions Avoided

- No product code, adapter code, CI, packaging, or environment systems were introduced prematurely.
- No exact host version lists were embedded into source directory doctrine.
- No unsupported parity claims were added.

### Remaining Issues

None for P00. Product implementation, inventory, scaffolding, harness, environments, evals, and packaging remain intentionally deferred to later prompts.

## Work Item: P06

### Status

Completed

### Changed Paths

- `specs/README.md`
- `specs/architecture/**`
- `shared/README.md`
- `shared/core/README.md`
- `shared/protocol/README.md`
- `shared/transforms/README.md`
- `shared/diagnostics/README.md`
- `shared/config/README.md`
- `shared/schemas/**`
- `shared/cli/README.md`
- `shared/local-service/README.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository already had governance, inventory, matrices, host-lane scaffolds, and host-family research. It did not yet have the contract architecture that explains how one shared core and many host adapters should actually fit together. P06 fills that gap before implementation begins.

### Notable Design Decisions

- Defined AIDE as a transport-agnostic shared core with thin host adapters.
- Standardized three execution modes: `embedded`, `cli-bridge`, and `local-service`.
- Defined stable contract objects for host identity, host context, document context, workspace context, selection context, feature requests, settings, diagnostics, capability reports, and adapter responses.
- Explicitly separated shared logic from host UI, packaging, runtime glue, and host-only policy exceptions.
- Kept schemas conservative and descriptive rather than over-engineering them into full validation systems before implementation pressure exists.

### Tradeoffs

- The architecture is intentionally structural and leaves several implementation details open, including concrete protocol serialization, service lifecycle mechanics, and feature-manifest file placement.
- The schemas stabilize core shape now, but they do not attempt exhaustive validation of every future edge case.

### Verification

- Verified existence of required `specs/architecture/` files, shared subtree directories, shared subtree `README.md` files, and schema files.
- Ran `rg` checks for required architecture anchors including:
  - `one shared core`
  - `many host adapters`
  - `embedded`
  - `cli-bridge`
  - `local-service`
  - `feature`
  - `settings`
  - `diagnostic`
  - `capability`
  - `request`
  - `response`
- Verified that `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P06 allowlist.

### Regressions Avoided

- No executable code, build scripts, CI, host-specific implementation files, or packaging manifests were added.
- The architecture does not pretend that any shared-core or adapter implementation already exists.
- The docs reuse the existing governance, support, and capability model instead of redefining them.

### Remaining Issues

- Concrete serialization format details, service lifecycle details, and per-feature manifests remain for later implementation prompts.
- No runtime validation or eval integration exists yet because this prompt was architecture-only.

## Work Item: P07

### Status

Completed

### Changed Paths

- `inventory/legal-acquisition.yaml`
- `environments/**`
- `labs/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository already tracked host families, capabilities, architecture, and research, but it did not yet have a durable framework for the environment-preservation side of long-horizon IDE work. P07 adds that control plane without pretending that media, snapshots, or runnable environments already exist.

### Notable Design Decisions

- Separated platform knowledge from concrete environment tracking by keeping `platforms/` distinct from `environments/`.
- Defined stable concepts for environment families, environment instances, install media, toolchains, snapshots, bootability, blockers, and archival records.
- Added a machine-readable legal and acquisition vocabulary in `inventory/legal-acquisition.yaml` rather than scattering provenance rules across prose files.
- Kept labs separate from environments so partial experiments, blocked bring-up work, and archival captures can progress without polluting stable environment catalogs.
- Reused explicit state language such as `planned`, `acquired`, `installing`, `boots`, `usable`, `blocked`, and `archival-record` to keep partial progress honest.

### Tradeoffs

- The catalogs intentionally stop at conservative structural shapes and empty records instead of inventing a real corpus.
- The framework leaves room for later environment-specific fields once actual bring-up work creates pressure for them.

### Verification

- Verified existence of required environment docs, environment subdirectories, catalog files, playbooks, lab docs, lab subdirectories, lab registers, and `inventory/legal-acquisition.yaml`.
- Ran `rg` checks for required anchors including:
  - `environment`
  - `install media`
  - `toolchain`
  - `snapshot`
  - `bootability`
  - `blocked`
  - `archival`
  - `official-download`
  - `local-only`
  - `planned`
  - `usable`
- Verified that `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P07 allowlist.

### Regressions Avoided

- No executable code, build scripts, CI, host-specific implementation files, or packaging manifests were added.
- No proprietary binaries, installers, images, or toolchains were checked into Git.
- No acquisition, ownership, or bootability facts were fabricated.

### Remaining Issues

- No actual environment instances, media records, toolchain records, or snapshots were populated in this prompt.
- Detailed bring-up results, local asset references, and blocker records remain for later prompts once real environment work begins.

## Work Item: P08

### Status

Completed

### Changed Paths

- `evals/**`
- `packaging/**`
- `matrices/test-matrix.yaml`
- `matrices/packaging-matrix.yaml`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository already had governance, research, architecture, environment control-plane records, and seed matrices. It did not yet have a durable framework for evaluation, verification, packaging posture, or release-shape tracking. P08 fills that gap without implying that executable tests, package builds, or shipped artifacts already exist.

### Notable Design Decisions

- Defined a layered evaluation model that separates structural verification, schema checks, documentation consistency checks, smoke categories, packaging checks, release-shape checks, and archival-record checks.
- Added machine-readable eval catalogs for eval definitions, verification routines, graders, and result states without fabricating real coverage.
- Defined a packaging model that separates artifact class, manifest family, signing posture, release channel, and release records from source layout.
- Kept source directory naming law intact while allowing future artifact names to include exact host versions where concrete release records justify them.
- Refined `matrices/test-matrix.yaml` and `matrices/packaging-matrix.yaml` into planning frameworks tied to stable family and technology ids rather than leaving them as shallow placeholders.

### Tradeoffs

- The catalogs emphasize structural shape and vocabulary now rather than prematurely introducing executable graders, manifests, or release records.
- Packaging posture is intentionally conservative and uses `unknown`, `deferred`, `planning-only`, or `archival-oriented` states where exact release mechanics remain unresolved.
- The evaluation matrix records planned posture only; it does not try to mimic test execution before implementation exists.

### Verification

- Verified existence of required `evals/` docs, subdirectories, playbooks, catalogs, and README files.
- Verified existence of required `packaging/` docs, subdirectories, catalogs, checklists, and README files.
- Verified existence of required YAML catalogs and refined matrix files.
- Ran `rg` checks for required anchors including:
  - `existence`
  - `schema`
  - `load-smoke`
  - `editor-smoke`
  - `workspace-smoke`
  - `packaging-check`
  - `release`
  - `native-extension-package`
  - `companion-package`
  - `stable`
  - `hotfix`
  - `verification`
  - `grader`
- Verified that `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P08 allowlist.

### Regressions Avoided

- No executable code, build scripts, CI, host-specific implementation files, signed artifacts, or release binaries were added.
- No matrix entry claims passing eval coverage or real packaging implementation that does not exist.
- No repository naming law was redefined; source layout remains technology-based.

### Remaining Issues

- No executable graders, smoke tests, release automation, manifest implementations, or package outputs were added in this prompt.
- Real run records, release records, and stronger coverage depend on later implementation and environment work.

## Work Item: P09

### Status

Completed

### Changed Paths

- `specs/boot-slice/**`
- `matrices/feature-coverage.yaml`
- `matrices/test-matrix.yaml`
- `evals/catalogs/eval-catalog.yaml`
- `evals/catalogs/verification-catalog.yaml`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository already had host research, capability posture, shared-core contracts, environment control-plane records, and eval scaffolding, but it still lacked one explicit first implementation target. P09 defines that target as a minimal cross-host boot slice and ties it to an honest oldest-first rollout plan.

### Notable Design Decisions

- Chose a two-part boot slice: universal `boot.slice.invoke` plus conditional `boot.slice.editor-marker`.
- Kept the first slice inside `L0` through `L2` and explicitly deferred `L3` and `L4`.
- Made the boot slice report-first and deterministic so every committed lane can participate without pretending to reach identical depth.
- Required `L2` editor proof only where the documented lane surface makes that the honest first proof, especially `xcodekit` and `vsix-v2-vssdk`.
- Applied oldest-first globally by lane phase and within families by exact version ids, while allowing companion fallback when a native or archival-native lane is blocked.

### Tradeoffs

- The rollout plan avoids a fake single-file chronological order across families whose archival dates are only partially reconstructed; it uses phase classes plus within-family version order instead.
- Some lanes with theoretical `L2` potential remain report-first or optional-marker lanes in the first wave to avoid making the entire rollout hostage to the hardest environment problems.
- The spec defines feature ids and behavior invariants now, but it intentionally stops short of adding new schemas or implementation stubs.

### Verification

- Verified existence of required `specs/boot-slice/` files, `boot-slice-manifest.yaml`, and `rollout-plan.yaml`.
- Ran `rg` checks for required anchors including:
  - `boot slice`
  - `host`
  - `lane`
  - `capability`
  - `fallback`
  - `blocked`
  - `oldest-first`
  - `verification`
- Verified that all committed lane paths appear in `specs/boot-slice/rollout-plan.yaml`.
- Verified that `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, and `evals/catalogs/verification-catalog.yaml` were updated.
- Verified that `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P09 allowlist.

### Regressions Avoided

- No implementation code, build scripts, CI, host-specific source files, or `.codex/` or `.agents/` content were added.
- The boot slice does not promise identical cross-host UX or universal `L2` depth.
- Blocked or degraded lanes are kept explicit rather than being erased from the rollout story.

### Remaining Issues

- No executable boot-slice implementation, run records, or passing eval results were added in this prompt.
- Exact environment blockers, packaging details, and lane-specific runtime glue remain for later implementation and lab prompts.

## Work Item: P10

### Status

Completed

### Changed Paths

- `shared/**`
- `fixtures/**`
- `evals/catalogs/eval-catalog.yaml`
- `evals/catalogs/verification-catalog.yaml`
- `evals/runs/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository had a defined shared-core contract and a concrete first boot-slice specification, but it still lacked any executable shared runtime. P10 turns that specification into a small deterministic implementation that later host adapters can call through an embedded path or a CLI bridge without forcing host-specific logic into the shared core.

### Notable Design Decisions

- Chose a pure Python 3 standard-library bootstrap runtime for this phase because it is sufficient for a deterministic shared-core proof and avoids unnecessary dependency or toolchain expansion.
- Implemented only the two boot-slice feature ids already defined by the spec: `boot.slice.invoke` and `boot.slice.editor-marker`.
- Kept lane-specific acceptance posture in a small static policy map under `shared/config/boot_slice.py` so the runtime can report honest fallback, optional, or required editor behavior without introducing host adapter code.
- Represented request envelopes, response envelopes, capability reports, and diagnostics as JSON-friendly dataclass-backed structures aligned to the existing shared schemas.
- Implemented a minimal `python -m shared.cli` bridge that accepts JSON from a file or stdin and emits deterministic JSON on stdout for later `cli-bridge` host work.
- Used committed JSON fixtures and standard-library `unittest` coverage as the first executable eval layer for the shared-core slice.

### Tradeoffs

- The runtime implements the boot-slice editor marker as a preview-only deterministic edit record rather than a general edit engine.
- Lane policy is static and conservative for this bootstrap phase; it reflects the current boot-slice acceptance table rather than a future dynamic registry.
- The shared core accepts the documented execution-mode values, but it does not implement a local-service daemon or any host integration lifecycle in P10.

### Verification

- Verified existence of shared-core implementation files under `shared/core/`, `shared/protocol/`, `shared/diagnostics/`, `shared/config/`, `shared/cli/`, and `shared/tests/`.
- Verified existence of deterministic request and response fixtures under `fixtures/boot-slice/`.
- Ran `py -3 -m unittest discover -s shared/tests -t .` and confirmed all tests passed.
- Ran `py -3 -m shared.cli --request fixtures\\boot-slice\\success-request.json --pretty` and confirmed the CLI smoke case passed with deterministic JSON output.
- Verified that `evals/catalogs/eval-catalog.yaml` and `evals/catalogs/verification-catalog.yaml` were updated for the shared-core slice.
- Verified that `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P10 allowlist.

### Regressions Avoided

- No `hosts/**` code, CI workflows, `.codex/` content, `.agents/` content, packaging automation, or external dependencies were added.
- No host-adapter success claims were made; the runtime reports shared-core capability only and keeps lane availability or fallback reasons explicit.
- No non-deterministic behavior, network calls, time-dependent behavior, or machine-local data was introduced into the fixtures or tests.

### Remaining Issues

- No host adapters call this runtime yet, so host-lane success remains deferred to later prompts.
- No local-service daemon, packaging flow, or broader feature set beyond the first boot slice was implemented.
- L3 and L4 behaviors, workspace awareness, and deeper IDE integration remain deferred by design.

## Work Item: P11

### Status

Completed

### Changed Paths

- `hosts/microsoft/**`
- `matrices/support-matrix.yaml`
- `matrices/capability-matrix.yaml`
- `matrices/feature-coverage.yaml`
- `matrices/test-matrix.yaml`
- `evals/catalogs/eval-catalog.yaml`
- `evals/catalogs/verification-catalog.yaml`
- `evals/runs/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

P10 proved the shared core and the host-agnostic CLI bridge, but no Microsoft host lane yet had a concrete first-wave proof. P11 turns the Microsoft rollout slice into explicit lane-local evidence while keeping business behavior in the shared core and staying honest about native archival or SDK blockers.

### Notable Design Decisions

- Reused the P10 shared-core CLI bridge for the first runnable Microsoft proofs instead of duplicating boot-slice behavior inside host lanes.
- Implemented lane-local `run_boot_slice.py` shims only where a thin `cli-bridge` proof is the accepted minimum and can run honestly in the current repository environment.
- Chose runnable degraded `L1` proofs for `com-addin`, `vsix-v1`, `extensibility`, and `visual-studio-mac/companion`.
- Chose explicit blocked structural proofs for `vsix-v2-vssdk` and `visual-studio-mac/monodevelop-addin` because those lanes require native or archival-native evidence that cannot be reproduced honestly here.
- Kept execution-mode choices conservative: `cli-bridge` for the runnable lanes, retained `embedded` as the intended target for `vsix-v2-vssdk`, and left `local-service` deferred for the modern extensibility lane.

### Tradeoffs

- The first Microsoft wave favors report-first or companion fallback evidence over premature native project scaffolding for lanes whose true toolchains are unavailable.
- `vsix-v2-vssdk` remains the Windows native reference target, but P11 stops at a blocked-proof record rather than inventing a fake native shell-hosted test.
- Visual Studio for Mac companion proof moves the family forward, but the native MonoDevelop-derived lane remains archival and blocked until preserved macOS assets exist.

### Verification

- Verified required Microsoft lane proof files and updated lane READMEs exist under `hosts/microsoft/**`.
- Ran `py -3 -m unittest discover -s shared/tests -t .` and confirmed the shared-core suite from P10 still passes.
- Ran lane-local runnable smoke checks:
  - `py -3 hosts\\microsoft\\visual-studio\\com-addin\\run_boot_slice.py --verify --pretty`
  - `py -3 hosts\\microsoft\\visual-studio\\vsix-v1\\run_boot_slice.py --verify --pretty`
  - `py -3 hosts\\microsoft\\visual-studio\\extensibility\\run_boot_slice.py --verify --pretty`
  - `py -3 hosts\\microsoft\\visual-studio-mac\\companion\\run_boot_slice.py --verify --pretty`
- Verified blocked structural evidence for non-runnable lanes through their committed request and blocked-proof records:
  - `hosts/microsoft/visual-studio/vsix-v2-vssdk/boot_slice_request.json`
  - `hosts/microsoft/visual-studio/vsix-v2-vssdk/blocked-proof.md`
  - `hosts/microsoft/visual-studio-mac/monodevelop-addin/boot_slice_request.json`
  - `hosts/microsoft/visual-studio-mac/monodevelop-addin/blocked-proof.md`
- Verified that Microsoft matrix rows, eval catalogs, and the Microsoft run record were updated.
- Verified that changed paths stayed inside the P11 allowlist and excluded an unrelated unstaged `README.md` change outside the prompt scope.

### Regressions Avoided

- No Apple or CodeWarrior host code was added.
- No shared-core business logic was duplicated or broadened beyond the P10 boot slice.
- No fake native build or runtime success was claimed for historical or SDK-bound lanes that were only structurally represented.
- No `.codex/`, `.agents/`, CI, or packaging automation content was introduced.

### Remaining Issues

- `vsix-v2-vssdk` still needs a real VSSDK-capable Visual Studio environment before an honest embedded `L2` editor-marker proof can be claimed.
- `extensibility` remains on a conservative `cli-bridge` proof; the documented local-service or richer out-of-process path is deferred.
- `visual-studio-mac/monodevelop-addin` remains blocked pending preserved macOS assets and a reproducible retired-host environment.
- Apple and CodeWarrior host implementations remain deferred to later prompts.

## Work Item: P12

### Status

Completed

### Changed Paths

- `hosts/apple/**`
- `matrices/support-matrix.yaml`
- `matrices/capability-matrix.yaml`
- `matrices/feature-coverage.yaml`
- `matrices/test-matrix.yaml`
- `evals/catalogs/eval-catalog.yaml`
- `evals/catalogs/verification-catalog.yaml`
- `evals/runs/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

P10 proved the shared core, and P11 established the first Microsoft host-lane wave, but Apple still had no concrete first-wave host proof. P12 turns the Apple rollout slice into explicit lane-local evidence while keeping shared behavior in the shared core and staying honest about native XcodeKit blockers outside a macOS or Xcode environment.

### Notable Design Decisions

- Reused the P10 shared-core CLI bridge for the first runnable Apple proof instead of duplicating boot-slice behavior inside Apple lanes.
- Implemented a thin `run_boot_slice.py` wrapper only for `hosts/apple/xcode/companion`, because that is the accepted runnable first proof in the current repository environment.
- Chose an explicit blocked structural proof for `hosts/apple/xcode/xcodekit` because the lane requires an embedded `L2` editor-marker proof that cannot be reproduced honestly without macOS or Xcode tooling.
- Added native-adjacent `extension-target.yaml` metadata for `xcodekit` to keep the Xcode Source Editor target shape visible without pretending it is build-verified.
- Kept execution-mode choices conservative: `cli-bridge` for the runnable companion lane and `embedded` as the intended but blocked target for `xcodekit`.

### Tradeoffs

- The Apple wave favors a runnable fallback proof plus a blocked native record instead of inventing a fake source-editor extension load outside macOS.
- `xcodekit` stays the Apple-native reference target, but P12 stops at blocked structural evidence rather than inventing a containing app, signing flow, or extension run that cannot be verified here.
- The companion lane moves older or broader Xcode workflows forward, but deeper project-aware behavior remains deferred.

### Verification

- Verified required Apple lane proof files and updated lane READMEs exist under `hosts/apple/**`.
- Ran `py -3 -B -m unittest discover -s shared/tests -t .` and confirmed the shared-core suite from P10 still passes.
- Ran the runnable Apple smoke check:
  - `py -3 hosts\\apple\\xcode\\companion\\run_boot_slice.py --verify --pretty`
- Verified blocked structural evidence for the non-runnable native lane through its committed request, target metadata, and blocked-proof records:
  - `hosts/apple/xcode/xcodekit/boot_slice_request.json`
  - `hosts/apple/xcode/xcodekit/extension-target.yaml`
  - `hosts/apple/xcode/xcodekit/blocked-proof.md`
- Verified that Apple matrix rows, eval catalogs, and the Apple run record were updated.
- Verified that changed paths stayed inside the P12 allowlist and excluded the unrelated unstaged `README.md` change outside the prompt scope.

### Regressions Avoided

- No Microsoft or CodeWarrior host code was added.
- No shared-core business logic was duplicated or broadened beyond the P10 boot slice.
- No fake native Xcode build, package, or runtime success was claimed for the blocked `xcodekit` lane.
- No `.codex/`, `.agents/`, CI, or packaging automation content was introduced.

### Remaining Issues

- `xcodekit` still needs a real macOS or Xcode environment plus a verified containing-app or extension packaging path before an honest embedded `L2` editor-marker proof can be claimed.
- The current shared-core bootstrap exposes the CLI bridge only; a verified embedded Swift or XcodeKit interop surface remains a later blocker rather than P12 scope.
- The Apple companion lane remains at an `L1` runnable fallback proof; broader project-aware workflows and native editor parity remain deferred.
- CodeWarrior host implementations remain deferred to later prompts.

## Work Item: P13

### Status

Completed

### Changed Paths

- `hosts/metrowerks/**`
- `inventory/legacy-ide-families.yaml`
- `matrices/support-matrix.yaml`
- `matrices/capability-matrix.yaml`
- `matrices/feature-coverage.yaml`
- `matrices/test-matrix.yaml`
- `evals/catalogs/eval-catalog.yaml`
- `evals/catalogs/verification-catalog.yaml`
- `evals/runs/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

P10 proved the shared core, P11 and P12 established the Microsoft and Apple host waves, but the committed legacy host family still had only research placeholders. P13 turns the CodeWarrior lanes into explicit boot-slice proofs and uses that implementation experience to tighten the broader legacy candidate backlog without promoting new families prematurely.

### Notable Design Decisions

- Reused the P10 shared-core CLI bridge for both committed CodeWarrior lanes instead of inventing legacy-specific business logic.
- Implemented a runnable archival-native `cli-bridge` proof for `hosts/metrowerks/codewarrior/ide-sdk` because the boot-slice acceptance for that lane is report-first `L1` with optional editor proof, and the shared lane map already supports that shape.
- Added `plugin-target.yaml` for `ide-sdk` so the native SDK or COM entry surface stays visible even though in-host loading remains unverified.
- Implemented a runnable fallback `cli-bridge` proof for `hosts/metrowerks/codewarrior/companion` to cover unresolved or non-native archival workflows outside the native lane.
- Stabilized `inventory/legacy-ide-families.yaml` by adding concise post-CodeWarrior next-action guidance instead of redesigning the backlog structure or promoting new host families.

### Tradeoffs

- The `ide-sdk` proof is intentionally report-first and stops at `L1`; it does not claim native IDE SDK loading, COM automation wiring, or the optional editor-marker path.
- The companion proof is runnable, but it does not replace the archival-native lane and does not imply project-aware behavior.
- Backlog stabilization stays conservative: it sharpens near-term versus difficult candidates through notes and next actions rather than inventing a new prioritization system.

### Verification

- Verified required CodeWarrior lane proof files and updated lane READMEs exist under `hosts/metrowerks/**`.
- Ran `py -3 -B -m unittest discover -s shared/tests -t .` and confirmed the shared-core suite from P10 still passes.
- Ran the runnable legacy smoke checks:
  - `py -3 hosts\\metrowerks\\codewarrior\\ide-sdk\\run_boot_slice.py --verify --pretty`
  - `py -3 hosts\\metrowerks\\codewarrior\\companion\\run_boot_slice.py --verify --pretty`
- Verified structural native-adjacent evidence for `ide-sdk` through `hosts/metrowerks/codewarrior/ide-sdk/plugin-target.yaml`.
- Verified that `inventory/legacy-ide-families.yaml`, legacy matrix rows, eval catalogs, and the CodeWarrior run record were updated.
- Verified that changed paths stayed inside the P13 allowlist and excluded the unrelated unstaged `README.md` change outside the prompt scope.

### Regressions Avoided

- No Microsoft or Apple host code was added.
- No shared-core logic was broadened or duplicated inside CodeWarrior lanes.
- No fake native CodeWarrior build, package, or in-host runtime success was claimed for the archival-native lane.
- No new committed legacy host families, `.codex/`, `.agents/`, CI, or packaging automation content were introduced.

### Remaining Issues

- `ide-sdk` still needs a reproducible historical environment before an honest in-host IDE SDK or COM automation proof can be claimed.
- The optional `boot.slice.editor-marker` proof for `ide-sdk` remains deferred until active-document capture is available from a real legacy environment.
- Later Eclipse-era CodeWarrior contract boundaries remain unresolved under the current `ide-sdk` umbrella.
- The broader legacy candidate backlog is still research-driven; P13 stabilizes it but does not promote any new family into `hosts/`.

## Work Item: P14

### Status

Completed

### Changed Paths

- `README.md`
- `CONTRIBUTING.md`
- `ROADMAP.md`
- `MAINTENANCE.md`
- `CHANGELOG.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `scripts/**`
- `.agents/README.md`
- `.agents/skills/**`
- `evals/reports/**`

### Rationale

The repository had completed its first planning, research, framework, and initial implementation waves, but the top-level docs still presented an earlier bootstrap picture and there was no dedicated maintenance baseline for future iterative work. P14 consolidates that state into a clearer contributor surface, a phase-based roadmap, reusable maintenance assets, repo-local maintenance skills, and a factual post-P13 audit.

### Notable Design Decisions

- Rewrote `README.md` to reflect post-P13 implementation reality rather than the earlier governance-only bootstrap state.
- Added `CONTRIBUTING.md`, `ROADMAP.md`, `MAINTENANCE.md`, and `CHANGELOG.md` as low-noise root control-plane docs rather than scattering contributor and maintenance guidance across multiple unrelated files.
- Kept maintenance automation at the control-plane level by creating task catalogs and checklists under `scripts/maintenance/` instead of adding CI or heavy executable automation.
- Added narrow repo-local skills for maintenance, docs normalization, roadmap work, and repo audits, following the existing `.agents/skills/` style.
- Added audit-style reports under `evals/reports/` so the completed bootstrap and first implementation wave has a concise factual rollup.

### Tradeoffs

- The new maintenance assets are intentionally procedural and mostly manual; they improve coherence now without pretending that automation maturity already exists.
- The roadmap stays phase-based and avoids dates, which is less specific than a schedule but more honest for the current repo state.
- The changelog is only a baseline template; it does not backfill earlier phases because that history already lives in `PLANS.md` and `IMPLEMENT.md`.

### Verification

- Verified existence of required root docs:
  - `CONTRIBUTING.md`
  - `ROADMAP.md`
  - `MAINTENANCE.md`
  - `CHANGELOG.md`
- Verified existence of required `scripts/maintenance/` files.
- Verified existence of required maintenance skill directories and `SKILL.md` files under `.agents/skills/`.
- Verified existence of `evals/reports/bootstrap-phase-audit.md`.
- Ran anchor scans for:
  - `roadmap`
  - `maintenance`
  - `blocked`
  - `deferred`
  - `candidate`
  - `committed`
  - `automation`
  - `audit`
  - `contributing`
  - `changelog`
- Ran `rg '^name:|^description:'` across the new maintenance-oriented skill files.
- Verified that `README.md`, `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` were updated.
- Verified that changed paths stayed inside the P14 allowlist.

### Regressions Avoided

- No product code, boot-slice expansion, new host adapters, CI workflows, or `.codex/` content were added.
- No roadmap dates or fabricated support claims were introduced.
- Blocked, deferred, candidate, and committed distinctions remain explicit.

### Remaining Issues

- Maintenance automation remains mostly manual and checklist-driven; later scripting or CI candidates are documented but not implemented here.
- The repository still carries major technical blockers in native host environments, packaging maturity, and broader release evidence; P14 documents them rather than resolving them.

## Work Item: P15

### Status

Completed

### Changed Paths

- `.aide/**`
- `.agents/skills/aide-queue/SKILL.md`
- `.agents/skills/aide-execplan/SKILL.md`
- `.agents/skills/aide-review/SKILL.md`
- `.agents/README.md`
- `.agents/skills/README.md`
- `scripts/aide-queue-next`
- `scripts/aide-queue-status`
- `scripts/aide-queue-run`
- `scripts/README.md`
- `docs/reference/self-bootstrap.md`
- `AGENTS.md`
- `README.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

### Rationale

The repository needed a minimal self-hosting control plane so future agent work can be resumed from filesystem state instead of relying on chat history or extension task queues. P15 creates that queue scaffold while preserving existing bootstrap-era phase records and implementation evidence.

### Notable Design Decisions

- Made `.aide/queue/` the canonical source of truth for non-trivial self-hosting work.
- Defined Q00 as a future baseline freeze and reboot audit rather than completing that audit in the bootstrap scaffold.
- Kept Q01 through Q04 as listed, pending queue items without task folders or implementation.
- Added autonomy, bypass, and review-gate policies as small YAML records rather than a full policy engine.
- Added queue scripts as read-only Python standard-library helpers with conservative line-oriented parsing.

### Tradeoffs

- The queue parser supports only the simple bootstrap `index.yaml` shape and is not a general YAML implementation.
- The runner script prints the next prompt but deliberately does not invoke Codex or any worker.
- The scaffold records the reboot focus on Contract, Harness, Compatibility, and Dominium Bridge without claiming that stack is implemented.

### Verification

- Verified required scaffold files exist.
- Ran Python syntax checks for `scripts/aide-queue-next`, `scripts/aide-queue-status`, and `scripts/aide-queue-run`.
- Ran `py -3 scripts/aide-queue-status`.
- Ran `py -3 scripts/aide-queue-next`.
- Ran `py -3 scripts/aide-queue-run`.
- Ran anchor scans for canonical queue, bypass, review-gate, ExecPlan, and Q00 language.
- Verified changed paths stayed inside the P15 allowlist.

### Regressions Avoided

- No product runtime, broker, service, host adapter, IDE extension, Commander, Mobile, app surface, provider integration, release action, tag, or package automation was added.
- No source code was moved.
- No forbidden implementation, governance, inventory, matrix, environment, lab, research, packaging, eval, fixture, shared, host, or spec paths were modified.
- Q01 through Q04 were not implemented.

### Remaining Issues

- Q00 still needs to be processed by a future worker and reviewed.
- Q01 through Q04 are queue placeholders only.
- Queue scripts are intentionally limited readers, not a full validator or autonomous runner.

## Work Item: Q00-bootstrap-audit

### Status

Needs Review

### Changed Paths

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/constitution/bootstrap-era-aide.md`
- `docs/charters/reboot-charter.md`
- `docs/reference/repo-census.md`
- `docs/roadmap/reboot-roadmap.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q00-bootstrap-audit/**`

### Rationale

Q00 freezes the current repository baseline for the in-place AIDE reboot. It records what bootstrap-era AIDE achieved, distinguishes implemented reality from future intent, and makes the Q01 through Q08 queue path visible without implementing later work.

### Notable Design Decisions

- Treated P00 through P15 as historical baseline rather than material to rewrite.
- Defined the reboot public model as AIDE Core, AIDE Hosts, and AIDE Bridges.
- Defined the internal Core split as Contract, Harness, Runtime, Compatibility, Control, and SDK.
- Recorded the first shipped stack as Contract + Harness + Compatibility + Dominium Bridge without claiming it is implemented.
- Expanded queue visibility through Q08 while creating no Q01 or later task folders.
- Kept Q00 review-gated and targeted for `needs_review` rather than self-approving it.

### Tradeoffs

- The repo census is a documentation map only; no source files were moved.
- The reboot roadmap is queue-oriented and does not add dates or release promises.
- Q00 evidence is structural and documentation-focused; it does not re-run heavy host or native tests.

### Verification

- Verified required Q00 deliverable files exist.
- Ran `py -3 scripts/aide-queue-status`; Q00 reported `needs_review`, and Q01 through Q08 were visible as planned pending items.
- Ran `py -3 scripts/aide-queue-next`; it reported `Q01-documentation-split`.
- Ran corrected anchor scans for `AIDE Core`, `AIDE Hosts`, `AIDE Bridges`, `Contract`, `Harness`, `Compatibility`, `Dominium Bridge`, `bootstrap-era`, and `pre-product`; all were found.
- Ran `py -3 -m py_compile scripts/aide-queue-next scripts/aide-queue-status scripts/aide-queue-run`; syntax check passed and generated bytecode was removed.
- Ran `git diff --check`; it passed with line-ending normalization warnings only.
- Ran an allowed-path audit; it passed with all changed paths inside the Q00 allowlist.
- Recorded validation details in `.aide/queue/Q00-bootstrap-audit/evidence/validation.md`.

### Regressions Avoided

- No bootstrap-era phase history was deleted or rewritten.
- No forbidden paths were modified.
- No Runtime, Commander, Mobile, IDE extension, app surface, provider integration, package, release, or autonomous worker implementation was added.
- Q01 through Q08 were not implemented.

### Remaining Issues

- Q00 requires review before being treated as accepted.
- Q01 through Q08 remain planned queue items.
- Runtime, CLI or Service surfaces, Commander, Mobile, IDE Hosts, packaging automation, and release work remain deferred.

## Work Item: Q01-documentation-split

### Status

Needs Review

### Changed Paths

- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/constitution/**`
- `docs/charters/**`
- `docs/roadmap/**`
- `docs/design-mining/**`
- `docs/decisions/**`
- `docs/reference/**`
- `.aide/queue/index.yaml`
- `.aide/queue/Q01-documentation-split/**`

### Rationale

Q01 makes the reboot documentation surface navigable before structural skeleton, contract, harness, compatibility, or bridge work begins. It preserves bootstrap-era records and maps them into durable document families instead of moving files.

### Notable Design Decisions

- Documented the public model as AIDE Core, AIDE Hosts, and AIDE Bridges.
- Documented the internal Core split as Contract, Harness, Runtime, Compatibility, Control, and SDK.
- Kept Runtime, SDK, IDE Hosts, Commander, Mobile, provider adapters, app surfaces, and automation as deferred or planned work.
- Created ADR-like decision records for the core reboot choices.
- Treated design-mining as future reference input, not doctrine.
- Stopped Q01 at `needs_review` because queue policy and Q00's status require review-gated continuation.

### Tradeoffs

- Q01 adds concise indexes and charters rather than a large final architecture rewrite.
- Documentation migration is a map and link strategy, not a file move.
- Command and generated-artifact references are intentionally minimal because Q03 through Q05 have not run.

### Verification

- Verified required Q01 documentation directories exist.
- Verified required charter files exist.
- Verified required decision records exist.
- Verified `README.md`, `DOCUMENTATION.md`, `ROADMAP.md`, `PLANS.md`, and `IMPLEMENT.md` contain Q01 documentation pointers.
- Ran `py -3 scripts/aide-queue-status`; Q00 and Q01 reported `needs_review`, and Q02 through Q08 remained pending.
- Ran `py -3 scripts/aide-queue-next`; it reported `Q02-structural-skeleton`.
- Ran terminology scans for AIDE Core, AIDE Hosts, AIDE Bridges, Contract, Harness, Runtime, Compatibility, Control, SDK, Dominium Bridge, XStack, bootstrap-era, and pre-product.
- Ran `git diff --check`; it passed with line-ending normalization warnings only.
- Ran an allowed-path audit; all changed paths stayed inside the Q01 allowlist.
- Recorded detailed validation in `.aide/queue/Q01-documentation-split/evidence/validation.md`.

### Regressions Avoided

- No source code, host lane, shared runtime, provider adapter, IDE extension, app surface, packaging, release, or heavy test work was added.
- No bootstrap-era phase history, research, eval, packaging, environment, governance, inventory, matrix, or host records were deleted or moved.
- No Q02 or later queue item was implemented.

### Remaining Issues

- Q01 requires review before being treated as accepted.
- Q00 is still `needs_review`, so Q01 records explicit follow-on authorization rather than assuming Q00 has passed.
- Q02 structural skeleton remains the next planned queue item and must be separately planned before implementation.

## Work Item: Q02-structural-skeleton

### Status

Needs Review

### Changed Paths

- `core/**`
- `hosts/README.md`
- `hosts/cli/**`
- `hosts/service/**`
- `hosts/commander/**`
- `hosts/extensions/**`
- `bridges/**`
- `docs/reference/structural-migration-map.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q02-structural-skeleton/**`

### Rationale

Q02 introduces the target structural skeleton for the in-place reboot while preserving the bootstrap-era implementation layout. It creates README-only homes for AIDE Core, AIDE Hosts, and AIDE Bridges and records how existing directories map to the future conceptual structure.

### Notable Design Decisions

- Created `core/**` as skeleton documentation only; no package files, imports, runtime logic, or migrated shared-core code were added.
- Added host-category skeletons under `hosts/cli/`, `hosts/service/`, `hosts/commander/`, and `hosts/extensions/` while preserving existing host proof lanes.
- Added `bridges/**` and Dominium Bridge placeholders without implementing bridge behavior.
- Added `docs/reference/structural-migration-map.md` to distinguish conceptual homes from current physical locations and move status.
- Kept XStack Dominium-local and did not broaden it into generic AIDE doctrine.

### Tradeoffs

- Q02 creates empty structural homes with README boundaries instead of moving current working code.
- Existing `shared/**` remains the executable bootstrap-era shared-core location until a later reviewed migration exists.
- Existing `scripts/**` and `shared/cli/**` remain in place even though they conceptually map toward future Harness and CLI host surfaces.

### Verification

- Verified required Q02 skeleton directories exist.
- Verified every required skeleton README exists.
- Verified `docs/reference/structural-migration-map.md` exists.
- Verified `README.md`, `DOCUMENTATION.md`, `ROADMAP.md`, `PLANS.md`, and `IMPLEMENT.md` contain Q02 structural pointers.
- Ran `py -3 scripts/aide-queue-status`; Q00, Q01, and Q02 reported `needs_review`, and Q03 remained pending.
- Ran `py -3 scripts/aide-queue-next`; it reported `Q03-profile-contract-v0`.
- Ran terminology scans for AIDE Core, AIDE Hosts, AIDE Bridges, Contract, Harness, Runtime, Compatibility, Control, SDK, Dominium Bridge, XStack, skeleton, and future move.
- Ran `py -3 -B -m unittest discover -s shared/tests -t .`; all 5 tests passed.
- Ran `git diff --check`; it passed with line-ending normalization warnings only.
- Ran an allowed-path audit; all changed paths stayed inside the Q02 allowlist.
- Recorded detailed validation in `.aide/queue/Q02-structural-skeleton/evidence/validation.md`.

### Regressions Avoided

- No existing source files, host proof files, tests, imports, scripts, evals, packaging records, governance records, inventory records, matrices, research, environments, or labs were moved or edited.
- No Q03 or later queue item was implemented.
- No Runtime, Service, Commander, Mobile, IDE extension implementation, provider adapter, app surface, generated artifact system, or autonomous service logic was added.

### Remaining Issues

- Q02 requires review before being treated as accepted.
- Q00 and Q01 remain `needs_review`; Q02 proceeded only because the current prompt explicitly authorized implementation.
- Q03 profile contract v0 remains the next planned queue item.

## Work Item: Q03-profile-contract-v0

### Status

Needs Review

### Changed Paths

- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/components/**`
- `.aide/commands/**`
- `.aide/policies/ownership.yaml`
- `.aide/policies/generated-artifacts.yaml`
- `.aide/policies/compatibility.yaml`
- `.aide/policies/validation-severity.yaml`
- `.aide/tasks/**`
- `.aide/evals/**`
- `.aide/adapters/**`
- `.aide/compat/**`
- `core/contract/**`
- `docs/reference/profile-contract-v0.md`
- `docs/reference/source-of-truth.md`
- `AGENTS.md`
- `.agents/skills/aide-queue/SKILL.md`
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q03-profile-contract-v0/**`

### Rationale

Q03 makes AIDE self-describing through a minimal declarative Profile/Contract v0. It records repo identity, lifecycle status, source-of-truth rules, component declarations, command posture, policies, task and eval declarations, adapter metadata, compatibility placeholders, and documented v0 shapes without implementing Harness behavior.

### Notable Design Decisions

- Kept Profile declarative and left executable Harness commands to Q04.
- Refined the existing P15 `.aide/profile.yaml` and `.aide/toolchain.lock` rather than treating them as absent.
- Used compact YAML catalogs under `.aide/` and Markdown shape docs under `core/contract/shapes/**`.
- Preserved existing autonomy, bypass, and review-gate policies without loosening them.
- Marked generated downstream artifacts as non-canonical outputs deferred to Q05.

### Tradeoffs

- Q03 uses documented YAML shapes rather than full JSON Schema or an executable validator because Python's standard library has no YAML or JSON Schema parser.
- Component ownership is conceptual and does not move bootstrap-era source files.
- Adapter records are metadata-only so the Profile does not overfit to any provider or host.

### Verification

- Verified required Q03 files and directories exist.
- Verified required component ids are declared.
- Verified command catalog distinguishes implemented queue scripts from planned Harness commands.
- Verified existing review gates were not loosened.
- Ran queue helper scripts.
- Ran terminology and source-of-truth scans.
- Ran lightweight YAML/Markdown sanity checks.
- Ran `git diff --check`.
- Ran an allowed-path audit.
- Recorded detailed validation in `.aide/queue/Q03-profile-contract-v0/evidence/validation.md`.

### Regressions Avoided

- No Q04 Harness commands were implemented.
- No generated downstream target artifacts were created.
- No source code was moved or refactored.
- No Runtime, Host, Commander, Mobile, IDE extension, provider adapter, app surface, package automation, release action, or autonomous service logic was added.
- No existing host proof, shared implementation, governance, inventory, matrix, research, environment, lab, eval, or packaging paths were modified.

### Remaining Issues

- Q03 requires review before being treated as accepted.
- Q00, Q01, and Q02 remain `needs_review`; Q03 proceeded only because the current prompt explicitly authorized implementation.
- Harness v0 remains Q04, generated artifacts remain Q05, compatibility baseline remains Q06, and Dominium Bridge baseline remains Q07.

## Work Item: Q04-harness-v0

### Status

Passed With Notes

### Changed Paths

- `scripts/aide`
- `core/harness/**`
- `docs/reference/harness-v0.md`
- `README.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q04-harness-v0/**`

### Rationale

Q04 implements the smallest executable Harness v0 over the Q03 declarative Profile/Contract. The Harness gives the repo a local command surface for structural validation, doctoring, compile-plan reporting, no-op migration posture, and bakeoff metadata readiness without implementing generated artifacts, Runtime, Hosts, providers, or service logic.

### Notable Design Decisions

- Used Python standard library only.
- Kept validation structural and text-based rather than claiming full YAML or schema validation.
- Kept `scripts/aide` as a thin repo-root wrapper and placed Harness logic under `core/harness/**`.
- Made `aide compile` report a deterministic plan only; generated artifacts remain Q05.
- Made `aide migrate` a no-op baseline report; compatibility baseline remains Q06.
- Made `aide bakeoff` metadata-only with no model, provider, native host, network, or external tool calls.
- Did not mutate final `.aide/` contract catalogs because this prompt allowed only Q04 queue/status/evidence changes under `.aide/`.

### Verification

- Ran Harness command smoke checks for `--help`, `init --dry-run`, `import`, `compile`, `validate`, `doctor`, `migrate`, and `bakeoff`.
- Ran lightweight Harness unittest smoke checks.
- Ran queue helper scripts.
- Checked generated target artifacts remained absent.
- Ran terminology searches.
- Ran `git diff --check`.
- Ran an allowed-path audit.
- Recorded detailed results in `.aide/queue/Q04-harness-v0/evidence/validation.md` and command output in `.aide/queue/Q04-harness-v0/evidence/command-smoke.md`.

### Regressions Avoided

- No Q05 generated artifacts were created.
- No `CLAUDE.md`, `.claude/**`, generated `.agents/skills/**` targets, provider targets, or generated downstream files were added.
- No Runtime, Service, Host, Commander, Mobile, IDE extension, provider, app, release, or autonomous worker implementation was added.
- No bootstrap-era source files, host proofs, governance, inventory, matrices, research, specs, environments, labs, evals, or packaging records were moved or edited.

### Remaining Issues

- Q04 review accepted Harness v0 with notes, so Q05 planning may proceed.
- Q05 implementation proceeded only after its own plan, generated-artifact source-of-truth rules, validation evidence requirements, and review gate were created.
- Q00 through Q03 remain `needs_review`; Q04 relied on explicit human authorization plus the foundation and full audit findings.
- `.aide/profile.yaml`, `.aide/toolchain.lock`, and `.aide/commands/catalog.yaml` were refreshed by Q05 under its bounded pre-generation scope.
- Full YAML/schema validation remains deferred.

## Work Item: Q05-generated-artifacts-v0

### Status

Needs Review

### Changed Paths

- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/commands/catalog.yaml`
- `.aide/generated/**`
- `AGENTS.md`
- `.agents/skills/aide-queue/SKILL.md`
- `.agents/skills/aide-execplan/SKILL.md`
- `.agents/skills/aide-review/SKILL.md`
- `core/harness/**`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/source-of-truth.md`
- `docs/reference/harness-v0.md`
- `README.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q05-generated-artifacts-v0/**`

### Rationale

Q05 gives the self-hosting repo a deterministic generated-artifact boundary for agent-facing guidance while preserving `.aide/` as the canonical Profile/Contract and `.aide/queue/` as the canonical long-running work queue.

### Notable Design Decisions

- Refreshed stale Q03-era Harness wording before generation because those records are source inputs.
- Kept `AGENTS.md` and the three existing AIDE skills as managed-section targets rather than full-file generated outputs.
- Generated Claude guidance only as `.aide/generated/preview/CLAUDE.md`; final root `CLAUDE.md` and final `.claude/**` remain deferred.
- Added `.aide/generated/manifest.yaml` with deterministic source and content fingerprints and no timestamps.
- Extended `aide compile` with `--dry-run`, `--preview`, and `--write`.
- Extended `aide validate` with generated marker, manifest, stale-source, and manual-edit checks while keeping validation structural and standard-library only.

### Tradeoffs

- Q05 v0 uses a small line-oriented manifest reader rather than full YAML parsing.
- Source-fingerprint drift is a warning/review-required condition in v0; marker/body mismatch is a hard error.
- Generated skill content is intentionally concise and does not create new broad skill families.

### Verification

- Ran pre-generation Harness validation, doctor, and compile checks.
- Ran `py -3 scripts/aide compile --dry-run`.
- Ran `py -3 scripts/aide compile --preview`.
- Ran `py -3 scripts/aide compile --write`.
- Ran post-generation Harness validation and command smoke checks.
- Ran lightweight Harness tests and Python syntax checks.
- Ran queue helper checks.
- Checked generated markers, manifest, and final Claude target absence.
- Ran `git diff --check`.
- Ran an allowed-path audit.

Detailed command output is recorded in `.aide/queue/Q05-generated-artifacts-v0/evidence/validation.md`.

### Regressions Avoided

- No final root `CLAUDE.md` or final `.claude/**` target was created.
- No generated artifact was made canonical truth.
- No Q06 Compatibility baseline, Q07 Dominium Bridge, Runtime, Host, Commander, Mobile, IDE extension, provider adapter, browser bridge, app surface, release automation, or autonomous service implementation was added.
- No forbidden bootstrap-era implementation, host proof, governance, inventory, matrix, research, spec, environment, lab, eval, or packaging path was modified.

### Remaining Issues

- Q05 requires review before generated artifact v0 is accepted.
- Q00 through Q03 remain `needs_review`.
- Full YAML/schema validation and the Compatibility baseline remain Q06 or later.
- Final Claude targets and broader generated skill families remain deferred pending review feedback.

## Work Item: Q06-compatibility-baseline

### Status

Needs Review

### Changed Paths

- `.aide/compat/**`
- `.aide/toolchain.lock`
- `.aide/commands/catalog.yaml`
- `.aide/evals/catalog.yaml`
- `.aide/generated/manifest.yaml`
- `core/compat/**`
- `core/harness/commands.py`
- `docs/reference/compatibility-baseline.md`
- `docs/reference/profile-contract-v0.md`
- `docs/reference/harness-v0.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/source-of-truth.md`
- `README.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/index.yaml`
- `.aide/queue/Q06-compatibility-baseline/**`

### Rationale

Q06 gives the self-hosting repo a first Compatibility baseline for evolution of AIDE contract, queue, Harness, generated-artifact, and compatibility metadata. The baseline is versioned and enforceable enough for future queue work, while remaining conservative and non-mutating.

### Notable Design Decisions

- Used AIDE string identifiers such as `aide.profile.v0` and `aide.compat-baseline.v0` instead of semver or dated versions.
- Added `.aide/compat/schema-versions.yaml` as the Q06 registry while preserving the older `.aide/compat/schema-version.yaml` for existing v0 readers.
- Added one no-op migration registry entry: `baseline-current-noop`.
- Defined replay as deterministic Harness summary expectations, not Runtime replay.
- Added upgrade gates that treat unknown future versions as errors and require review for schema or generated-artifact contract changes.
- Added deprecation record format with no active deprecations.
- Extended `aide validate` and `aide migrate` with structural compatibility checks only.

### Tradeoffs

- Q06 still does not parse full YAML or enforce JSON Schema.
- `aide migrate` reports compatibility posture and available no-op migrations but has no apply mode.
- Generated artifact behavior was not changed; the existing Q05 `aide compile --write` path was used only to refresh the manifest after Q06 changed source inputs.
- `.aide/profile.yaml` still contains Q05-era current-focus wording because it was not in the Q06 implementation allowlist.

### Verification

- Ran pre-change `py -3 scripts/aide validate`, `doctor`, `compile`, and `migrate`.
- Ran post-change `py -3 scripts/aide validate`, `doctor`, `migrate`, `compile`, and `bakeoff`.
- Ran Harness and Compatibility unittest discovery.
- Ran Python syntax checks for Harness, Compatibility, and `scripts/aide`.
- Ran queue helper checks.
- Ran compatibility record existence and anchor checks.
- Ran `git diff --check`.
- Ran an allowed-path audit.

Detailed command output is recorded in `.aide/queue/Q06-compatibility-baseline/evidence/validation.md`.

### Regressions Avoided

- No real migrations, migration apply mode, Runtime, Host, Commander, Mobile, IDE extension, provider, browser, app, release, service, or Dominium Bridge behavior was added.
- No generated target policy was changed and no final `CLAUDE.md` or `.claude/**` target was created.
- No bootstrap-era implementation, host proof, governance, inventory, matrix, research, spec, environment, lab, top-level eval, or packaging path was modified.

### Remaining Issues

- Q06 requires review before Compatibility baseline v0 is accepted.
- Q00 through Q03 and Q05 still have raw `needs_review` queue statuses; Q05 review evidence is `PASS_WITH_NOTES` and explicitly allowed Q06.
- Full YAML/schema validation, real migrations, shims, and compatibility replay beyond summary anchors remain later work.
- Dominium Bridge baseline remains Q07.

## Work Item: Q07-dominium-bridge-baseline

### Status

Needs Review

### Changed Paths

- `bridges/dominium/**`
- `core/harness/**`
- `.aide/components/catalog.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/evals/catalog.yaml`
- `docs/reference/dominium-bridge.md`
- `docs/reference/compatibility-baseline.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/source-of-truth.md`
- `docs/charters/bridges-charter.md`
- `README.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q07-dominium-bridge-baseline/**`
- `.aide/queue/index.yaml`

### Rationale

Q07 establishes the first AIDE-side Dominium Bridge baseline so Dominium can later consume AIDE as a pinned portable repo layer under XStack strict governance.

### Notable Design Decisions

- Kept the bridge AIDE-side only; no external Dominium repository paths were touched.
- Kept XStack Dominium-local and strict rather than promoting it into generic AIDE doctrine.
- Used `pinned-managed-repo-layer` as the near-term adoption mode.
- Added a profile overlay and strict policy overlays rather than replacing `.aide/profile.yaml` or weakening base AIDE policy.
- Recorded generated target classes as metadata only; no real Dominium outputs were emitted.
- Referenced the Q06 Compatibility baseline and Q05 generated artifact ids without creating a separate bridge version system.
- Added only structural Harness bridge checks and compile-plan reporting.

### Tradeoffs

- Bridge validation remains line-oriented and structural, not full YAML/schema validation.
- Dominium-side adoption, pins, generated outputs, and proof execution remain future work.
- Q07 records stricter XStack expectations but does not implement XStack internals.
- The Q05 generated manifest remains stale because Q07 changed generated-artifact source inputs and this task did not refresh generated outputs.

### Verification

- Ran pre-change Harness validation, doctor, compile, and migrate checks.
- Ran post-change Harness validation, doctor, compile dry-run, migrate, and bakeoff checks.
- Ran Harness and Compatibility unittest discovery.
- Ran Python syntax checks for Harness, Compatibility, and `scripts/aide`.
- Ran queue helper checks.
- Checked required Dominium Bridge files and structural anchors.
- Checked generated artifact drift and confirmed no real Dominium outputs were emitted.
- Ran `git diff --check`.
- Ran an allowed-path audit.

Detailed command output is recorded in `.aide/queue/Q07-dominium-bridge-baseline/evidence/validation.md`.

### Regressions Avoided

- No external Dominium repository was modified.
- No real Dominium generated output was emitted.
- No Runtime, Host, Commander, Mobile, IDE extension, provider adapter, browser bridge, app surface, release automation, service, or autonomous worker implementation was added.
- No Q08 or later work was implemented.

### Remaining Issues

- Q07 requires independent review before Q08 planning or Dominium-side adoption work.
- Q05 generated manifest source fingerprint is stale because Q07 changed source inputs and did not run `aide compile --write`.
- `.aide/profile.yaml` still contains Q05/Q06-era high-level wording; cleanup remains deferred to a later reviewed task.

## Work Item: Q07 Dominium Bridge Baseline Review

### Status

Passed with notes.

### Changed Paths

- `.aide/queue/Q07-dominium-bridge-baseline/evidence/review.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-validation.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-risks.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-recommendation.md`
- `.aide/queue/Q07-dominium-bridge-baseline/status.yaml`
- `.aide/queue/index.yaml`
- `PLANS.md`

### Rationale

Record the independent Q07 review outcome and mark the canonical queue state so Q08 planning can proceed from a passed Dominium Bridge baseline.

### Notable Design Decisions

- Accepted Q07 as `PASS_WITH_NOTES` rather than `PASS` because generated manifest drift and stale summary/doctor guidance remain visible cleanup items.
- Marked Q07 `passed` in queue state because Q07 `status.yaml` allowed the transition and the review prompt permitted Q07 status/index updates.
- Did not refresh generated artifacts because the review task forbids generated artifact mutation.

### Verification

- Ran `py -3 scripts/aide --help`, `validate`, `doctor`, `compile --dry-run`, `migrate`, and `bakeoff`.
- Ran Harness and Compatibility unittest discovery.
- Ran Python syntax checks for Harness, Compatibility, and `scripts/aide`.
- Ran queue helper checks.
- Checked bridge files, anchors, policy strictness, generated-output absence, dependency/scope boundaries, compile determinism, `git diff --check`, and review allowed paths.

Detailed command output is recorded in `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-validation.md`.

### Regressions Avoided

- No Dominium Bridge, Harness, Compatibility, generated artifact, Runtime, Host, provider, release, app, or Q08 implementation files were modified by the review.
- No external Dominium repository was touched.
- No real Dominium generated outputs were emitted.

### Remaining Issues

- `.aide/generated/manifest.yaml` remains stale by source fingerprint and should be refreshed only by a reviewed generated-artifact task.
- `aide doctor` still prints Q07 review as the next recommended step after Q07 is passed; this should be cleaned up before automation treats doctor output as an execution signal.
- Q00-Q03, Q05, and Q06 raw queue statuses remain review-gated even though later review evidence accepted proceeding with notes.

## Work Item: Q08 Self-Hosting Automation

### Status

Needs Review

### Changed Paths

- `core/harness/**`
- `scripts/aide-queue-next`
- `scripts/aide-queue-run`
- `.aide/runs/self-check/latest.md`
- `docs/reference/self-hosting-automation.md`
- `docs/reference/self-bootstrap.md`
- `docs/reference/harness-v0.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/compatibility-baseline.md`
- `docs/reference/dominium-bridge.md`
- `docs/reference/source-of-truth.md`
- `README.md`
- `ROADMAP.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q08-self-hosting-automation/**`
- `.aide/queue/index.yaml`

### Rationale

Q08 adds the first safe self-hosting automation scaffold so AIDE can inspect its own queue, drift, Compatibility, and bridge state without becoming an uncontrolled autonomous runtime.

### Notable Design Decisions

- Added `aide self-check` to the existing Harness command surface rather than adding a new service or external worker runner.
- Kept self-check report-first by default, with explicit `--write-report` limited to `.aide/runs/self-check/latest.md`.
- Fixed stale doctor next-step guidance by computing the next recommendation from Q08 queue state.
- Improved `scripts/aide-queue-next` and `scripts/aide-queue-run` so they report review-gate posture instead of failing or implying automatic execution.
- Reported stale generated manifest drift and recommended a reviewed generated-artifact QFIX instead of refreshing `.aide/generated/manifest.yaml`.

### Verification

- Ran pre-change Harness validation, doctor, compile dry-run, migrate, bakeoff, queue-status, and queue-next checks.
- Ran post-change Harness validation, doctor, compile dry-run, migrate, bakeoff, self-check, and self-check report writing.
- Ran `scripts/aide --help`, `scripts/aide import`, queue helper smoke checks, Harness tests, Compatibility tests, PowerShell-expanded Python syntax checks, generated artifact absence checks, dependency/scope scans, and `git diff --check`.

Detailed command output is recorded in `.aide/queue/Q08-self-hosting-automation/evidence/validation.md`.

### Regressions Avoided

- No external agents, models, providers, browsers, network calls, or external CI were introduced.
- No generated artifacts were refreshed.
- No Runtime, Service, Commander, Host, Mobile, app, release, package, or autonomous worker implementation was added.
- No Dominium repository or real Dominium generated output was touched.

### Remaining Issues

- Q08 requires independent review.
- `.aide/generated/manifest.yaml` remains stale by source fingerprint and should be refreshed only by a reviewed generated-artifact QFIX.
- `.aide/commands/catalog.yaml` does not yet list `aide self-check`; Q08 left that metadata sync deferred because `.aide/commands/**` was outside the implementation allowed paths.
- Q00-Q03, Q05, and Q06 raw queue-status nuance remains visible and unresolved.

## Work Item: Q08 Self-Hosting Automation Review

### Status

Passed With Notes

### Changed Paths

- `.aide/queue/Q08-self-hosting-automation/evidence/review.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/review-validation.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/review-risks.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/review-recommendation.md`
- `.aide/queue/Q08-self-hosting-automation/status.yaml`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

### Rationale

The Q08 independent review accepted the report-first self-hosting automation scaffold as safe for post-Q08 foundation review while preserving visible cleanup notes for generated manifest drift, command catalog metadata, and older raw status nuance.

### Verification

- Ran Harness command smoke for `--help`, `validate`, `doctor`, `compile --dry-run`, `migrate`, `bakeoff`, `self-check`, and `self-check --write-report`.
- Ran queue helper smoke for `aide-queue-status`, `aide-queue-next`, and `aide-queue-run`.
- Ran Harness and Compatibility unit tests.
- Ran Python syntax checks for Harness, Compatibility, and queue helper scripts.
- Ran safety scans for external calls, automatic worker invocation, auto-merge, and generated artifact refresh behavior.
- Ran `git diff --check`.

Detailed command output is recorded in `.aide/queue/Q08-self-hosting-automation/evidence/review-validation.md`.

### Regressions Avoided

- No self-hosting automation implementation, Harness implementation, queue helper implementation, generated artifacts, contract catalogs, Runtime, Host, Commander, provider, browser, app, release, external CI, or post-Q08 implementation files were modified by the review.
- No generated artifacts were refreshed.
- No external worker or Dominium repository was touched.

### Remaining Issues

- `.aide/generated/manifest.yaml` remains stale by source fingerprint and should be refreshed only by a reviewed generated-artifact QFIX.
- `.aide/commands/catalog.yaml` still does not list `aide self-check`; a bounded metadata sync should handle this before the next horizon.
- Q00-Q03, Q05, and Q06 raw queue-status nuance remains visible and should be reconciled or explicitly documented before the next horizon.

## Work Item: Q09 State Reconciliation And Token Survival Core

### Status

Needs Review

### Changed Paths

- `.aide/queue/Q09-token-survival-core/**`
- `.aide/queue/index.yaml`
- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/commands/catalog.yaml`
- `.aide/policies/**`
- `.aide/prompts/**`
- `.aide/context/**`
- `.aide/memory/**`
- `.aide/scripts/**`
- `AGENTS.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `DOCUMENTATION.md`
- `docs/reference/**`
- `core/harness/**`

### Rationale

Q09 starts the post-Q08 token-survival horizon. The immediate product constraint is that AIDE must reduce token usage and charges for equivalent-quality work, so this phase reconciles stale current-state records and adds compact repo-derived task packets, approximate token estimates, evidence-review prompts, and no-full-history guidance.

### Notable Design Decisions

- Keep Q09 repo-only and no-install; Gateway, provider calls, model routing, Runtime, Service, Commander, Mobile, MCP/A2A, and autonomous loops remain deferred.
- Preserve older raw queue status nuance instead of silently rewriting Q00-Q03, Q05, or Q06.
- Treat `.aide/runs/self-check/latest.md` as non-canonical evidence and prefer fresh command output for live state.
- Use Python standard library only for AIDE Lite token-survival tooling.
- Store generated Q09 context outputs under `.aide/context/` without inlining source contents; the formal token ledger remains deferred to Q14.
- Relocate unit tests to `core/harness/tests` because Python unittest cannot import hidden `.aide/scripts/tests` with the requested `-t .` discovery shape.

### Verification

Baseline validation passed before edits. Q09 generated `.aide/context/latest-task-packet.md` for Q10 at 2,587 chars and 647 approximate tokens. Detailed final command output is recorded in `.aide/queue/Q09-token-survival-core/evidence/validation.md`.

### Regressions Avoided

- No provider/model/network calls were added.
- No Gateway, Runtime, Service, Commander, Mobile, MCP/A2A, host implementation, app surface, or autonomous loop was added.
- No raw provider credentials, local caches, `.aide.local` data, or raw prompt logs were committed.

### Remaining Issues

- Q09 awaits independent review.
- Token counts are approximate only.
- AIDE Lite still needs Q10 hardening for drift detection and stronger validation.
- Context compiler, verifier, ledger, golden tasks, router profile, cache boundary, and Gateway remain later phases.

## Work Item: Q10 AIDE Lite Hardening

### Status

Needs Review

### Changed Paths

- `.aide/queue/Q10-aide-lite-hardening/**`
- `.aide/queue/index.yaml`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_lite.py`
- `.aide/context/repo-snapshot.json`
- `.aide/context/latest-task-packet.md`
- `.aide/commands/catalog.yaml`
- `.aide/generated/manifest.yaml`
- `AGENTS.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/reference/**`
- `docs/roadmap/**`
- `core/harness/tests/test_aide_lite.py`

### Rationale

Q10 makes the Q09 token-survival workflow repeatable enough to become the default path for future AIDE queue prompts. AIDE Lite now has stronger validation, deterministic writes, adapter drift handling, snapshot summaries, packet budget warnings, importable helpers, and direct stdlib tests.

### Notable Design Decisions

- Keep AIDE Lite standard-library only and repo-local; no provider, model, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, or host behavior was added.
- Use generated `AGENTS.md` markers consistent with existing AIDE generated-section conventions while preserving manual content outside the managed section.
- Replace legacy Q09 token-survival markers only because they are managed output.
- Keep approximate `chars / 4` token counts; exact tokenizer and provider billing remain deferred.
- Keep context compilation shallow until Q11; Q10 snapshots record metadata and hashes only, not file contents.
- Keep direct `.aide/scripts/tests` discovery as the supported no-install test shape because Python `-t .` discovery is awkward for hidden `.aide` import names.

### Verification

Q10 validation covered Harness validate/doctor/self-check, Harness and Compatibility unit tests, AIDE Lite doctor/validate/snapshot/pack/estimate/adapt/selftest, direct `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q10-aide-lite-hardening/evidence/validation.md`.

### Regressions Avoided

- No long-history prompt storage, raw provider credentials, `.aide.local` state, local caches, or raw prompt logs were committed.
- No Gateway, provider router, live model calls, local model setup, exact tokenizer, provider billing ledger, full verifier, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host implementation, or autonomous loop was introduced.
- No generated artifact manifest was hand-edited; it was refreshed through `scripts/aide compile --write` after command catalog/index changes.

### Remaining Issues

- Q10 awaits independent review.
- Token estimates remain approximate only.
- Context compiler, verifier, token ledger, golden tasks, router profile, cache boundary, and Gateway remain later phases.
- Python unittest discovery with `-s .aide/scripts/tests -t .` remains a documented hidden-path limitation; direct `.aide/scripts/tests` discovery passes.

## Work Item: Q11 Context Compiler v0

### Status

Needs Review

### Changed Paths

- `.aide/queue/Q11-context-compiler-v0/**`
- `.aide/queue/index.yaml`
- `.aide/context/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_lite.py`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/memory/project-state.md`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/reference/**`
- `docs/roadmap/**`
- `core/harness/tests/test_aide_lite.py`

### Rationale

Q11 reduces prompt size by replacing broad repo/history context with deterministic repo maps, test maps, context indexes, latest context packets, exact refs, and context-backed task packets.

### Notable Design Decisions

- Kept the Context Compiler standard-library only and deterministic.
- Used path and extension heuristics for role detection; no semantic certainty is claimed.
- Used test path/name heuristics with confidence and reason fields; no complete coverage is claimed.
- Kept generated context artifacts content-free: refs, hashes, sizes, roles, priorities, counts, and test candidates only.
- Added `path#Lstart-Lend` validation without full excerpt extraction.
- Left `.aide/generated/manifest.yaml` drift visible because Q11 does not allow generated manifest edits.

### Verification

Q11 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/pack/estimate/adapt/selftest, direct `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q11-context-compiler-v0/evidence/validation.md`.

### Regressions Avoided

- No raw source contents, secrets, `.env` content, local state, `.aide.local` data, caches, provider credentials, or raw prompt logs were committed.
- No Gateway, provider calls, live model routing, local model setup, exact tokenizer, provider billing ledger, embeddings, vector search, semantic cache, full verifier, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host implementation, or autonomous loop was introduced.

### Remaining Issues

- Q11 awaits independent review.
- Role classification and test mapping remain heuristics.
- Token counts remain approximate only.
- Q12 verifier, Q14 token ledger, Q15 golden tasks, router profile, cache boundary, and Gateway remain later phases.

## Work Item: Q12 Verifier v0

### Status

Needs Review

### Changed Paths

- `.aide/queue/Q12-verifier-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/verification.yaml`
- `.aide/verification/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/**`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/evidence-review.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/memory/project-state.md`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- `README.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `docs/reference/**`
- `docs/roadmap/**`
- `core/harness/tests/test_aide_verifier.py`

### Rationale

Q12 reduces premium-model review burden by moving structural checks into deterministic AIDE Lite verifier behavior. Future GPT-5.5 review can consume compact verifier output and evidence instead of re-checking packet sections, refs, scope, adapter drift, token warnings, or obvious secret risks.

### Notable Design Decisions

- Kept the verifier standard-library only and repo-local.
- Used conservative file-ref extraction from backticks and markdown links rather than trying to parse arbitrary prose.
- Kept changed-file scope path-based against the active queue task; no semantic diff analysis is claimed.
- Treated secret scanning as heuristic and allowed policy terms when they do not resemble real key values.
- Wrote compact verification reports without raw file contents.

### Verification

Q12 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/pack/estimate/verify variants/selftest, direct `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q12-verifier-v0/evidence/validation.md`.

### Regressions Avoided

- No raw source dumps, secrets, `.env` contents, `.aide.local` state, local caches, provider credentials, or raw prompt logs were committed.
- No Gateway, provider calls, live model routing, local model setup, exact tokenizer, provider billing ledger, LLM-as-judge, automatic repair, golden tasks, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host implementation, or autonomous loop was introduced.

### Remaining Issues

- Q12 awaits independent review.
- Verification remains structural, path-based, and heuristic.
- Token counts remain approximate only.
- Q13 Evidence Review Workflow, Q14 token ledger, Q15 golden tasks, router profile, cache boundary, and Gateway remain later phases.

## Work Item: Q13 Evidence Review Workflow

### Status

Needs Review.

### Changed Paths

- `.aide/queue/Q13-evidence-review-workflow/**`
- `.aide/queue/index.yaml`
- `.aide/verification/review-packet.template.md`
- `.aide/verification/review-decision-policy.yaml`
- `.aide/policies/verification.yaml`
- `.aide/prompts/evidence-review.md`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/**`
- `.aide/context/**`
- `.aide/memory/project-state.md`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- root docs and selected `docs/reference/**` / `docs/roadmap/**`

### Rationale

Q13 reduces premium-model review burden by producing a compact review packet that references task packets, context packets, verifier reports, evidence files, changed-file summaries, validation summaries, token summaries, risks, and non-goals. GPT-5.5 review can now start from `.aide/context/latest-review-packet.md` instead of re-reading full chat history, whole repo docs, or broad roadmap context.

### Notable Design Decisions

- Kept review-pack deterministic, standard-library only, and repo-local.
- Generated review packets contain references and compact summaries, not full source files or full diffs.
- Added `verify --review-packet` so malformed review packets are checked mechanically before review.
- Added decision policy rules for `PASS`, `PASS_WITH_NOTES`, `REQUEST_CHANGES`, and `BLOCKED`.
- Left automatic GPT/model calls explicitly out of scope.

### Verification

Q13 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/pack/estimate/selftest, review-packet verification, direct `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q13-evidence-review-workflow/evidence/validation.md`.

### Regressions Avoided

- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host implementation, LLM-as-judge automation, automatic GPT review, automatic repair, or autonomous loop was introduced.
- No raw source dumps, full diffs, secrets, `.env` content, local state, `.aide.local` data, caches, provider credentials, or raw prompt logs were committed.

### Remaining Issues

- Q13 awaits independent review.
- Review packet quality depends on evidence quality.
- Token counts remain approximate only.
- Q14 token ledger, Q15 golden tasks, router profile, cache boundary, and Gateway remain later phases.

## Work Item: Q14 Token Ledger and Savings Report

### Status

Needs Review.

### Changed Paths

- `.aide/queue/Q14-token-ledger-savings-report/**`
- `.aide/queue/index.yaml`
- `.aide/policies/token-ledger.yaml`
- `.aide/policies/token-budget.yaml`
- `.aide/reports/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_token_ledger.py`
- `.aide/context/**`
- `.aide/verification/latest-verification-report.md`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/evidence-review.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/memory/project-state.md`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- root docs and selected `docs/reference/**` / `docs/roadmap/**`

### Rationale

Q14 makes AIDE's token-saving claim measurable. It records estimated metadata for compact packets, verification reports, evidence surfaces, prompt templates, generated guidance, and named naive baselines so future phases can compare compact repo-derived packets against broader prompt bundles without storing raw prompts or raw responses.

### Notable Design Decisions

- Kept token accounting deterministic, standard-library only, and repo-local.
- Used `ceil(chars / 4)` as the explicit approximation method; exact tokenizer and provider billing remain deferred.
- Stored metadata-only JSONL records with path, surface, chars, lines, approximate tokens, budget, budget status, and notes.
- Added named baselines for root-history, review, repo-context, and token-survival comparisons.
- Added budget status values and advisory regression warnings without making Q14 a billing system or quality eval system.
- Integrated ledger readiness into AIDE Lite doctor, validate, estimate, pack, context, review, verify, and selftest behavior where bounded.

### Verification

Q14 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger scan/ledger report/ledger compare/pack/estimate/selftest, direct `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q14-token-ledger-savings-report/evidence/validation.md`.

### Regressions Avoided

- No raw prompt bodies, raw response bodies, provider credentials, `.env` contents, `.aide.local` state, local caches, provider billing records, or exact-token claims were committed.
- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host implementation, LLM-as-judge automation, automatic GPT review, automatic repair, golden tasks, or autonomous loop was introduced.

### Remaining Issues

- Q14 awaits independent review.
- Token counts remain approximate only.
- The ledger does not measure provider billing, hidden reasoning tokens, cached-token discounts, or quality outcomes.
- Q15 golden tasks, router profile, cache boundary, and Gateway remain later phases.

## Work Item: Q15 Golden Tasks v0

### Status

Needs Review.

### Changed Paths

- `.aide/queue/Q15-golden-tasks-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/evals.yaml`
- `.aide/evals/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_golden_tasks.py`
- `.aide/reports/**`
- `.aide/context/**`
- `.aide/prompts/compact-task.md`
- `.aide/prompts/evidence-review.md`
- `.aide/prompts/codex-token-mode.md`
- `.aide/memory/project-state.md`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- root docs and selected `docs/reference/**` / `docs/roadmap/**`

### Rationale

Q15 makes AIDE's quality-preservation claim measurable for the token-saving workflow. Q14 can show that compact artifacts are smaller; Q15 checks that the smaller artifacts still include required sections, references, evidence shape, verifier failure detection, review-packet shape, token-ledger metadata, and adapter managed-section determinism.

### Notable Design Decisions

- Kept golden tasks deterministic, standard-library only, repo-local, and free of model/provider/network calls.
- Added six initial golden tasks for compact task packets, context packets, verifier bad-evidence detection, review packets, token ledger metadata, and managed adapter determinism.
- Stored eval reports as deterministic metadata and Markdown summaries under `.aide/evals/runs/`.
- Integrated `eval list`, `eval run`, and `eval report` into AIDE Lite doctor, validate, selftest, and ledger scan/report behavior.
- Treated token reduction as invalid when golden tasks fail, while explicitly not claiming arbitrary coding quality or external benchmark coverage.

### Verification

Q15 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger scan/ledger report/eval list/eval run/eval report/pack/estimate/selftest, direct `.aide/scripts/tests` discovery, documented hidden-directory discovery behavior, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q15-golden-tasks-v0/evidence/validation.md`.

### Regressions Avoided

- No raw prompts, raw responses, provider credentials, `.env` contents, `.aide.local` state, local caches, exact-token claims, or provider billing records were committed.
- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, external benchmark integration, LLM-as-judge, automatic GPT review, automatic repair, Q16 recommendation engine, or autonomous loop was introduced.

### Remaining Issues

- Q15 awaits independent review.
- Golden tasks are deterministic local quality gates for AIDE's token-survival substrate, not arbitrary coding-task quality proof.
- Token counts remain approximate only.
- Q16 Outcome Controller, Router Profile, cache boundary, and Gateway remain later phases.

## Work Item: Q16 Outcome Controller v0

### Status

Needs Review.

### Changed Paths

- `.aide/queue/Q16-outcome-controller-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/controller.yaml`
- `.aide/controller/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_outcome_controller.py`
- `.aide/scripts/tests/test_review_pack.py`
- `.aide/context/**`
- `.aide/reports/**`
- `.aide/evals/runs/**`
- `.aide/prompts/**`
- `.aide/memory/**`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- root docs and selected `docs/reference/**` / `docs/roadmap/**`

### Rationale

Q16 makes AIDE's self-optimization posture advisory, measured, and review-gated. It reads local token, verifier, review-packet, golden-task, context, and adapter signals and converts them into concrete recommendations without applying them automatically.

### Notable Design Decisions

- Kept the controller deterministic, standard-library only, repo-local, and free of model/provider/network calls.
- Added `.aide/policies/controller.yaml` and `.aide/controller/failure-taxonomy.yaml` to define allowed inputs, outputs, failure classes, recommendation requirements, and forbidden behaviors.
- Stored outcome records as metadata-only JSONL under `.aide/controller/outcome-ledger.jsonl`.
- Added `outcome add`, `outcome report`, and `optimize suggest` to AIDE Lite.
- Required recommendations to include evidence source, expected benefit, risk level, next action, rollback condition, and `applies_automatically: false`.
- Treated Q17 Router Profile as the next advisory phase only; no routing, Gateway, provider, or Runtime behavior was introduced.

### Verification

Q16 validation covered Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger scan/ledger report/eval list/eval run/eval report/outcome report/outcome add/optimize suggest/pack/estimate/selftest, direct `.aide/scripts/tests` discovery, documented hidden-directory discovery behavior, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q16-outcome-controller-v0/evidence/validation.md`.

### Regressions Avoided

- No raw prompts, raw responses, provider credentials, `.env` contents, `.aide.local` state, local caches, exact-token claims, provider billing records, or raw model traces were committed.
- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, automatic prompt/policy/route mutation, automatic GPT review, automatic repair, Router Profile behavior, or autonomous loop was introduced.

### Remaining Issues

- Q16 awaits independent review.
- Recommendations are local and heuristic; they are inputs to future queue work, not an automatic optimizer.
- Token counts remain approximate only.
- Q17 Router Profile, Q18 cache/local-state boundary, Gateway/provider/runtime/UI work, and model/provider evals remain later phases.

## Work Item: Q17 Router Profile v0

### Status

Needs Review.

### Changed Paths

- `.aide/queue/Q17-router-profile-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/routing.yaml`
- `.aide/models/**`
- `.aide/routing/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_router_profile.py`
- `.aide/context/**`
- `.aide/reports/**`
- `.aide/prompts/**`
- `.aide/memory/**`
- `.aide/commands/catalog.yaml`
- `AGENTS.md`
- root docs and selected `docs/reference/**` / `docs/roadmap/**`

### Rationale

Q17 makes AIDE's future model/tool choice evidence-based before any live routing
exists. It reads compact task/context packets and local verifier, token,
golden-task, review, and outcome signals, then writes advisory route decisions
with a route class, hard-floor status, quality gates, evidence sources, and
fallback guidance.

### Notable Design Decisions

- Kept routing deterministic, standard-library only, repo-local, and free of model/provider/network calls.
- Added `.aide/policies/routing.yaml` plus advisory `.aide/models/**` metadata for providers, capabilities, route profiles, hard floors, and fallbacks.
- Added `.aide/routing/latest-route-decision.json` and `.aide/routing/latest-route-decision.md` as metadata-only route artifacts.
- Added `route list`, `route validate`, and `route explain` to AIDE Lite.
- Preserved hard floors for architecture, security, self-modification, final promotion, governance, destructive, and high-stakes work.
- Routed deterministic work toward `no_model_tool` and unknown work conservatively toward frontier or human review.

### Verification

Q17 validation covered Harness validate/doctor/self-check, Harness and
Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify
/review-pack/ledger scan/ledger report/eval list/eval run/eval report/outcome
report/optimize suggest/route list/route validate/route explain/pack/estimate
/selftest, direct `.aide/scripts/tests` discovery, documented hidden-directory
discovery behavior, `git diff --check`, and targeted secret scanning. Detailed
command output is recorded in
`.aide/queue/Q17-router-profile-v0/evidence/validation.md`.

### Regressions Avoided

- No raw prompts, raw responses, provider credentials, `.env` contents, `.aide.local` state, local caches, exact-token claims, provider billing records, or raw model traces were committed.
- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, automatic prompt/policy/route mutation, automatic GPT review, automatic repair, cache boundary, or autonomous loop was introduced.

### Remaining Issues

- Q17 awaits independent review.
- Route heuristics are conservative and local; they are route advice, not execution.
- Provider capabilities are advisory metadata only; no live availability probing or current pricing exists.
- Token counts remain approximate only.
- Q18 cache/local-state boundary, Gateway/provider/runtime/UI work, and model/provider evals remain later phases.

## Work Item: Q18 Cache and Local State Boundary

### Status

Implemented and awaiting review.

### Changed Paths

- `.gitignore`
- `.aide.local.example/**`
- `.aide/policies/cache.yaml`
- `.aide/policies/local-state.yaml`
- `.aide/cache/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_cache_local_state.py`
- `.aide/queue/Q18-cache-local-state-boundary/**`
- `.aide/queue/index.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/prompts/**`
- `.aide/memory/**`
- root docs and `docs/reference/cache-local-state-boundary.md`

### Rationale

Q18 prevents future Gateway, provider, runtime, and cache work from mixing committed AIDE contract records with machine-local runtime state. It creates deterministic cache-key metadata now while explicitly deferring live cache behavior.

### Notable Design Decisions

- `.aide/` remains committed contract and reviewable metadata.
- `.aide.local/` is gitignored local runtime state and must not be tracked.
- `.aide.local.example/` documents the safe layout without secrets.
- Cache reports store SHA-256 metadata, dependency hashes, policy versions, and dirty-state notes only.
- Cache hits do not bypass verifier, golden tasks, route hard floors, or review gates.
- Semantic cache for code edits and provider response cache remain disabled until future reviewed policy.

### Verification

Q18 validation covers Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger/eval/outcome/route/cache/pack/estimate/selftest, cache unit tests, `git check-ignore .aide.local/`, `git diff --check`, and targeted secret scanning. Detailed command output is recorded in `.aide/queue/Q18-cache-local-state-boundary/evidence/validation.md`.

### Regressions Avoided

- No actual `.aide.local/` contents were committed.
- No raw prompts, raw responses, provider response bodies, semantic answers, traces, local cache blobs, provider credentials, `.env` contents, exact-token claims, or provider billing records were committed.
- No model, provider, network, Gateway, Runtime, Service, Commander, UI, Mobile, MCP/A2A, automatic prompt/policy/route mutation, automatic GPT review, automatic repair, live cache, or autonomous loop was introduced.

### Remaining Issues

- Q18 awaits independent review.
- Cache keys are deterministic metadata only and do not prove stale content is safe to reuse.
- No live Gateway, provider response cache, semantic cache, exact tokenizer, provider billing integration, local model KV cache, or runtime cache service exists.
- Q19 Gateway Architecture and Skeleton remains the next bounded phase.

## Work Item: Q19 Gateway Architecture and Skeleton

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/policies/gateway.yaml`
- `.aide/gateway/**`
- `core/gateway/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_gateway_commands.py`
- `.aide/queue/Q19-gateway-architecture-skeleton/**`
- `.aide/queue/index.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/prompts/**`
- `.aide/memory/**`
- root docs and `docs/reference/gateway-skeleton.md`

### Rationale

Q19 creates a safe local Gateway boundary after Q09-Q18 established compact
context, verification, review packets, token accounting, golden tasks,
advisory outcomes, advisory routes, cache keys, and local-state policy. It
exposes those local signals before any provider adapter or live proxy exists.

### Notable Design Decisions

- Added `.aide/policies/gateway.yaml` with local skeleton, report-only, and
  no-provider-forwarding operating mode.
- Added `.aide/gateway/` architecture, endpoint, lifecycle, security-boundary,
  and latest-status artifacts.
- Added `core/gateway/gateway_status.py` for compact health, status, route,
  summaries, and version payloads.
- Added `core/gateway/server.py` as a localhost-only stdlib HTTP skeleton.
- Added AIDE Lite `gateway status`, `gateway endpoints`, `gateway smoke`, and
  `gateway serve`.
- Integrated Gateway readiness into AIDE Lite validation, doctor, verification,
  review-packet summaries, and selftest.

### Verification

Q19 validation covers Harness validate/doctor/self-check, Harness and
Compatibility tests, core Gateway tests, AIDE Lite
doctor/validate/snapshot/index/context/verify/review-pack/ledger/eval/outcome/
optimize/route/cache/gateway/pack/estimate/selftest, Gateway endpoint smoke,
`git check-ignore .aide.local/`, `git diff --check`, and targeted secret
scanning. Detailed command output is recorded in
`.aide/queue/Q19-gateway-architecture-skeleton/evidence/validation.md`.

### Regressions Avoided

- No provider calls, model calls, outbound network calls, or real Gateway proxy
  forwarding were introduced.
- No OpenAI-compatible or Anthropic-compatible forwarding endpoints were
  implemented.
- No raw prompts, raw responses, provider credentials, `.env` contents,
  `.aide.local` state, local traces, or real cache blobs were committed.
- No Runtime, Service, Commander, UI, Mobile, MCP/A2A, provider adapter, or
  autonomous loop was introduced.

### Remaining Issues

- Q19 awaits independent review.
- The skeleton is not a production Gateway and has no authentication,
  authorization, live route execution, service manager, provider adapters,
  provider billing, or exact tokenizer.
- Q20 Provider Adapter v0 remains the next bounded phase and must still respect
  `.aide.local/`, no raw prompt/response storage, verifier/golden-task gates,
  and Gateway safety policy.

## Work Item: Q20 Provider Adapter v0

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/policies/provider-adapters.yaml`
- `.aide/providers/**`
- `core/providers/**`
- `core/gateway/gateway_status.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_provider_adapter.py`
- `.aide/queue/Q20-provider-adapter-v0/**`
- `.aide/queue/index.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/prompts/**`
- `.aide/memory/**`
- root docs and `docs/reference/provider-adapter-v0.md`

### Rationale

Q20 defines provider adapters as offline contracts before any live provider
execution exists. Provider routing can reduce token waste only when provider
families, privacy posture, credential boundaries, capability metadata, and
hard-floor rules are explicit and testable.

### Notable Design Decisions

- Added `.aide/policies/provider-adapters.yaml` with offline-contracts-only,
  metadata-validation-only, and no-provider-calls operating mode.
- Added `.aide/providers/` catalog, capability matrix, adapter contract, static
  status, and latest provider status reports.
- Added `core/providers/**` standard-library dataclasses, catalog parsing,
  validation, status rendering, and offline probe helpers.
- Added AIDE Lite `provider list`, `provider status`, `provider validate`,
  `provider contract`, and `provider probe --offline`.
- Integrated provider readiness into AIDE Lite validation, verification,
  doctor, selftest, review-packet summaries, advisory route notes, and Gateway
  status summaries.

### Verification

Q20 validation covers Harness validate/doctor/self-check, Harness,
Compatibility, Gateway, and Provider tests, AIDE Lite
doctor/validate/snapshot/index/context/verify/review-pack/ledger/eval/outcome/
optimize/route/cache/gateway/provider/pack/estimate/selftest,
`git check-ignore .aide.local/`, `git diff --check`, and targeted secret
scanning. Detailed command output is recorded in
`.aide/queue/Q20-provider-adapter-v0/evidence/validation.md`.

### Regressions Avoided

- No live provider calls, model calls, outbound network calls, provider probes,
  credential setup, or Gateway forwarding were introduced.
- No raw prompts, raw responses, provider credentials, `.env` contents,
  `.aide.local` state, local traces, provider response caches, or real cache
  blobs were committed.
- No Runtime, Service, Commander, UI, Mobile, MCP/A2A, local model setup,
  provider billing, exact tokenizer, automatic GPT review, automatic repair, or
  autonomous loop was introduced.

### Remaining Issues

- Q20 awaits independent review.
- Capability metadata is conservative contract metadata, not measured provider
  performance, availability, pricing, latency, or quality evidence.
- Future live provider work still needs explicit reviewed phases for
  credentials, provider probes, Gateway forwarding, provider response caching,
  billing, and exact capability validation.
- Q21 Existing Tool Adapter Compiler v0 remains the next bounded phase.

## Work Item: QFIX-01 Foundation Review Reconciliation

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/QFIX-01-foundation-review-reconciliation/**`
- `.aide/queue/index.yaml`
- `.aide/queue/Q09-token-survival-core/status.yaml` and `evidence/review.md`
- `.aide/queue/Q10-aide-lite-hardening/status.yaml` and `evidence/review.md`
- `.aide/queue/Q11-context-compiler-v0/status.yaml` and `evidence/review.md`
- `.aide/queue/Q12-verifier-v0/status.yaml` and `evidence/review.md`
- `.aide/queue/Q13-evidence-review-workflow/status.yaml` and `evidence/review.md`
- `.aide/queue/Q14-token-ledger-savings-report/status.yaml` and `evidence/review.md`
- `.aide/queue/Q15-golden-tasks-v0/status.yaml` and `evidence/review.md`
- `.aide/queue/Q16-outcome-controller-v0/status.yaml` and `evidence/review.md`
- `.aide/queue/Q17-router-profile-v0/status.yaml` and `evidence/review.md`
- `.aide/queue/Q18-cache-local-state-boundary/task.yaml`, `status.yaml`, and `evidence/review.md`
- `.aide/queue/Q19-gateway-architecture-skeleton/status.yaml` and `evidence/review.md`
- `.aide/queue/Q20-provider-adapter-v0/status.yaml` and `evidence/review.md`
- `.aide/profile.yaml`
- `.aide/commands/catalog.yaml`
- `core/harness/commands.py`
- `core/harness/tests/test_aide_harness.py`
- root docs

### Rationale

QCHECK found that Q09-Q20 existed and mostly worked, but future agents would
still waste context on stale source-of-truth records. QFIX-01 accepts the
token-survival foundation with notes, fixes Q18 drift, updates profile and
self-check guidance, and records QFIX-02 as the next repair before Q21.

### Reconciliation Decisions

- Q09-Q20 are accepted with notes, not marked flawless.
- Q18 task/status drift is fixed.
- `.aide/profile.yaml` now describes the post-token-foundation reconciliation
  state rather than stale Q09 focus.
- `scripts/aide self-check` no longer recommends stale Q09 once Q09-Q20 are
  accepted.
- Gateway and provider surfaces remain no-call/report-only or offline metadata.

### Verification

Baseline validation before edits covered Harness validate/doctor/self-check,
AIDE Lite doctor/validate/verify/eval/route/cache/provider checks, Harness,
Compatibility, Gateway, and Provider tests, and the known failing
`.aide/scripts/tests` discovery command. Final validation is recorded in
`.aide/queue/QFIX-01-foundation-review-reconciliation/evidence/validation.md`.

### Remaining Issues

- QFIX-01 itself still requires review.
- QFIX-02 must repair standard `.aide/scripts/tests` discovery and a routine
  runner.
- Token savings remain estimated, not billing truth.
- Golden tasks remain substrate quality gates, not arbitrary coding-task proof.
- Cross-repo pack export/import and Eureka/Dominium pilots remain future work.

## Work Item: QFIX-02 AIDE Lite Test Discovery And Runner Fix

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/**`
- `.aide/queue/index.yaml`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_lite.py`
- `.aide/commands/catalog.yaml`
- `core/harness/commands.py`
- `core/harness/tests/test_aide_harness.py`
- `docs/reference/aide-lite.md`
- `docs/reference/aide-lite-test-runner.md`
- root docs

### Rationale

The QCHECK audit and QFIX-01 evidence showed that the AIDE Lite suite passed
when run with the direct discovery form but failed under
`py -3 -m unittest discover -s .aide/scripts/tests -t .`. That failure made
validation feel broken even though the tests were healthy. QFIX-02 makes
`py -3 .aide/scripts/aide_lite.py test` the canonical validation command and
documents the old `-t .` form as non-canonical for the hidden `.aide` path.

### Implementation Notes

- Added `test` as a stable alias over the existing internal selftest runner.
- Preserved `selftest` as a compatibility command.
- Added tests for import-without-CLI-side-effects, `test` pass behavior,
  controlled failure return code, command catalog truth, and Harness next-step
  guidance while QFIX-02 is active.
- Kept the supported raw unittest command as
  `py -3 -m unittest discover -s .aide/scripts/tests`.
- Did not add package markers under `.aide/` or move AIDE Lite into a Python
  package.

### Verification

Final validation is recorded in
`.aide/queue/QFIX-02-aide-lite-test-discovery-runner/evidence/validation.md`.
Key checks include Harness validate/doctor/self-check, AIDE Lite
doctor/validate/test/selftest, supported `.aide/scripts/tests` discovery,
Harness/Compatibility/Gateway/Provider tests, `git diff --check`, and targeted
secret scans.

### Remaining Issues

- QFIX-02 itself still requires review.
- The old `-t .` discovery command remains invalid/non-canonical by design.
- Q21 Cross-Repo Pack Export / Import v0 is next after QFIX-02 review.
- Token savings remain estimated, and no arbitrary coding-task quality proof is
  introduced.
- No Gateway/provider/model runtime behavior is introduced.

## Work Item: Q21 Cross-Repo Pack Export / Import v0

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/Q21-cross-repo-pack-export-import-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/export-import.yaml`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/import/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_export_import.py`
- `.aide/commands/catalog.yaml`
- `.aide/prompts/codex-token-mode.md`
- root docs and `docs/reference/cross-repo-pack-export-import.md`

### Rationale

Q21 makes the token-survival foundation portable before the first real
Eureka/Dominium pilots. It prevents manual broad copying from contaminating
target repos with AIDE source identity, queue history, generated context,
reports, latest status artifacts, local state, raw prompts, raw responses, or
secrets.

### Notable Design Decisions

- Added `.aide/policies/export-import.yaml` to define the portable pack
  include/exclude boundary.
- Added `.aide/import/**` target-neutral templates for profile, project state,
  decisions, open risks, and import reports.
- Added AIDE Lite `export-pack`, `import-pack`, and `pack-status` commands.
- Generated `.aide/export/aide-lite-pack-v0/` with manifest, checksums, install
  docs, import policy, export report, and portable `files/`.
- Import preserves manual `AGENTS.md` content through a managed portable
  section, creates target-specific placeholders when absent, and ensures
  `.aide.local/` remains ignored.
- Fixture validation uses temporary local repositories only; real Eureka and
  Dominium imports remain Q22/Q23.

### Verification

Q21 validation covers Harness validate/doctor/self-check, AIDE Lite
doctor/validate/test/selftest/export-pack/pack-status/import-pack dry-run and
import, fixture target doctor/snapshot/index/pack/estimate, AIDE Lite
export/import unit tests, Harness/Compatibility/Gateway/Provider tests,
`git check-ignore .aide.local/`, `git diff --check`, and targeted secret
scanning. Detailed command output is recorded in
`.aide/queue/Q21-cross-repo-pack-export-import-v0/evidence/validation.md`.

### Regressions Avoided

- No real Eureka or Dominium repositories were mutated.
- No source repo `.aide/profile.yaml`, `.aide/queue/**`, source memory,
  generated context, reports, controller ledgers, route/cache/Gateway/provider
  latest status artifacts, eval runs, `.aide.local/`, `.env`, secrets, raw
  prompts, or raw responses were copied into the portable pack.
- No provider calls, model calls, network calls, Gateway forwarding, Runtime,
  Service, Commander, UI, Mobile, MCP/A2A, existing-tool adapter compiler, or
  autonomous loop was introduced.

### Remaining Issues

- Q21 awaits independent review.
- Fixture import proves portability mechanics only; Q22 and Q23 must measure
  real target-repo token savings and quality preservation.
- Target-specific profile and memory placeholders still require human or
  project-specific completion after import.
- Exact tokenizer, provider billing, live provider execution, and existing-tool
  adapter compiler work remain deferred.

## Work Item: Q24 Existing Tool Adapter Compiler v0

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/Q24-existing-tool-adapter-compiler-v0/**`
- `.aide/queue/index.yaml`
- `.aide/policies/adapters.yaml`
- `.aide/adapters/**`
- `.aide/generated/adapters/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_adapter_compiler.py`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/commands/catalog.yaml`
- `.aide/prompts/**`
- root docs and `docs/reference/existing-tool-adapter-compiler-v0.md`

### Rationale

Most AIDE users will reach AIDE first through existing coding tools rather than
through a future Gateway or Service. Q24 compiles AIDE's compact-packet,
context, validation, evidence, review-gate, local-state, and no-provider-call
rules into concise tool-specific guidance for Codex, Claude Code, Aider, Cline,
Continue, Cursor, and Windsurf.

### Implementation Notes

- Added `.aide/policies/adapters.yaml` for template-compiler-only operation,
  generated or preview outputs, managed-section rules, drift detection, and
  no-runtime/no-provider/no-network safety.
- Added `.aide/adapters/targets.yaml` and templates for Codex/AGENTS, Claude
  Code, Aider, Cline, Continue, Cursor, and Windsurf.
- Added AIDE Lite `adapter list`, `adapter render`, `adapter preview`,
  `adapter validate`, `adapter drift`, and `adapter generate` commands.
- Kept `adapt` backward-compatible as a deterministic shortcut for the safe
  `AGENTS.md` managed section.
- Generated adapter previews under `.aide/generated/adapters/**` and updated
  only the managed section in root `AGENTS.md`.
- Updated the portable AIDE Lite Pack to include adapter templates and policy
  so target repos can generate local guidance after import.

### Verification

Final validation is recorded in
`.aide/queue/Q24-existing-tool-adapter-compiler-v0/evidence/validation.md`.
Key checks include Harness validate/doctor/self-check, AIDE Lite
doctor/validate/test/selftest, adapter list/render/preview/validate/drift,
deterministic `adapt`, export-pack refresh, AIDE Lite adapter compiler tests,
full AIDE Lite test discovery, Harness/Compatibility/Gateway/Provider tests,
`git diff --check`, `.aide.local/` ignore verification, and targeted secret
scan.

### Remaining Issues

- Q24 itself still requires review.
- Q22 and Q23 target-pilot evidence is now present in the sibling Eureka and
  Dominium repositories and awaits target-repo review. Q24 evidence was
  refreshed read-only to record those pilot results, but generated adapter
  outputs still need target-tool usage evidence.
- Non-AGENTS tool outputs are preview-only.
- Generated guidance is advisory and depends on each tool reading it.
- Exact tokenizer, provider billing, live provider execution, Gateway
  forwarding, IDE extensions, and runtime enforcement remain deferred.

## Work Item: Q24 Post-Pilot Evidence Refresh

### Status

Evidence and documentation refresh completed; Q24 remains `needs_review`.

### Notes

- Inspected `D:\Projects\Eureka\eureka` read-only and found
  `EUREKA-AIDE-PILOT-01` at `needs_review` with a 948 approximate-token task
  packet versus a 68,647 approximate-token baseline.
- Inspected `D:\Projects\Dominium\dominium` read-only and found
  `DOMINIUM-AIDE-PILOT-01` at `needs_review` with a 1,087 approximate-token
  task packet versus a 110,115 approximate-token doctrine-heavy baseline.
- Updated Q24 evidence and compact root docs to stop saying target-pilot
  evidence is absent.
- Did not change adapter compiler code, templates, targets, generated root/tool
  outputs, Gateway/provider behavior, or any Eureka/Dominium file.

## Work Item: Q25 Importer Scope And State Truth Repair

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/Q25-importer-scope-and-state-truth-repair/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_export_import.py`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/import/**`
- `.aide/policies/export-import.yaml`
- `.aide/profile.yaml`
- `.aide/commands/catalog.yaml`
- `core/harness/commands.py`
- `core/harness/tests/test_aide_harness.py`
- root docs and `docs/reference/cross-repo-pack-export-import.md`

### Rationale

The cross-repo readiness audit showed that AIDE had real target-pilot
token-reduction evidence, but broad handoff was blocked by pack-status failure,
stale pack provenance, an importer that planned optional broad roots by
default, and state surfaces that still pointed at QFIX/Q21-era next work.

### Implementation Notes

- Changed pack checksums to cover payload and static pack docs while excluding
  mutable `manifest.yaml`, `checksums.json`, and `export-report.md` metadata.
- Regenerated `.aide/export/aide-lite-pack-v0/` so `pack-status` passes.
- Made `import-pack` default to safe mode, report exact dry-run planned writes,
  skip optional broad `core/` and `docs/` roots by default, and keep `--mode
  full` explicit for reviewed local fixtures.
- Preserved manual `AGENTS.md` merge behavior and target-specific profile or
  memory template generation.
- Refreshed `.aide/profile.yaml`, command catalog truth, and Harness
  self-check guidance so Q25 review or Q26 handover is now recommended instead
  of stale QFIX-02/Q21 followups.
- Generated the Q26 Eureka Pilot Review And Handover task packet.

### Verification

Q25 validation covers AIDE Lite export/import tests, canonical AIDE Lite test,
export-pack regeneration, pack-status, import-pack dry-run/write into temporary
fixtures, imported fixture doctor/snapshot/index/pack, Harness
validate/doctor/self-check, Harness/Compatibility/Gateway/Provider tests,
`git diff --check`, `.aide.local/` ignore verification, and targeted secret
scan. Detailed command output is recorded in
`.aide/queue/Q25-importer-scope-and-state-truth-repair/evidence/validation.md`.

### Remaining Issues

- Q25 itself requires review before Q26 Eureka handover.
- Fixture import proves the safer importer behavior but does not replace target
  pilot review.
- Dominium-specific golden tasks, exact tokenizer/provider billing, live
  Gateway/provider runtime, and broad adapter-output target-tool usage evidence
  remain future work.

## Work Item: Q25 Fix-Forward Pack Integrity Revalidation

### Status

Implemented and awaiting review as part of Q25.

### Notes

- Added the missing documentation-only `.aide.local.example/secrets/README.md`
  required by the Q18 local-state validation surface.
- Kept real `secrets/**` ignored while adding a narrow `.gitignore` exception
  only for `.aide.local.example/secrets/README.md`.
- Tightened `validate_pack_checksums` so `pack-status` fails if a payload file
  exists in the export pack without a checksum entry.
- Added tests for unchecksummed payload detection and for exporting the safe
  local-state secrets README.
- Regenerated `.aide/export/aide-lite-pack-v0/`; the pack now reports 123
  included files, 126 checksums, and `pack-status` passes.
- Re-ran safe import dry-run/write fixtures; safe mode planned/wrote 106 files,
  skipped optional broad roots, preserved manual `AGENTS.md`, imported the safe
  secrets README, and did not copy `core/` or `docs/`.

### Verification

Final verification used
`C:\Program Files\Hybrid\64bit\Vapoursynth\python.exe` (Python 3.12.9).
AIDE Lite validate/test, export-pack, pack-status, import fixtures,
`.aide/scripts/tests` discovery, Harness/Compatibility/Gateway/Provider tests,
Q26 task-packet generation, diff check, ignore checks, and targeted secret
scans passed. The later Q26 handover refresh regenerated the Harness
generated manifest; remaining Harness warnings are review gates rather than
Q25 pack/import blockers.

## Work Item: Q26 Eureka Pilot Review And Handover

### Status

Implemented and awaiting review.

### Changed Paths

- `.aide/queue/Q26-eureka-pilot-review-and-handover/**`
- `.aide/queue/index.yaml`
- `.aide/queue/Q27-commit-discipline-workunit-recovery-v0/**`
- `.aide/queue/Q28-git-workflow-policy-v0/**`
- `.aide/queue/Q29-merge-land-promote-helper-v0/**`
- `.aide/profile.yaml`
- `core/harness/commands.py`
- `.aide/context/latest-task-packet.md`
- `.aide/generated/manifest.yaml`
- root docs

### Rationale

After Q25 repaired pack integrity, provenance, and safe import scope, AIDE still
had no explicit Q26 review packet and still showed Q27-Q29 as active blockers
from the pre-repair state. Q26 records the Eureka pilot handover checkpoint and
clears those stale active blockers without pretending Q27-Q29 are implemented.

### Implementation Notes

- Added the Q26 queue packet, evidence, status, prompt, and ExecPlan.
- Reviewed the sibling Eureka repository read-only and recorded current pilot
  evidence and validation posture.
- Marked earlier Q27, Q28, and Q29 blocked attempts as superseded redo records.
- Updated profile and self-check guidance so the next sequence is Q25 review,
  Q26 review, then Q27 Commit Discipline And WorkUnit Recovery v0 redo.
- Regenerated the latest task packet for Q27 redo.
- Refreshed the generated manifest after source-truth changes.

### Verification

Q26 validation covers AIDE Harness validate/doctor/self-check, AIDE Lite
validate/test/pack-status, read-only Eureka doctor/validate/task estimate,
Eureka diff and architecture checks, diff check, `.aide.local/` ignore checks,
and targeted secret scans. Detailed command output is recorded in
`.aide/queue/Q26-eureka-pilot-review-and-handover/evidence/validation.md`.

### Remaining Issues

- Q25 and Q26 require review before their outputs are accepted.
- Q27, Q28, and Q29 are not implemented; their old blocked attempts are only
  superseded so they can be redone from the repaired baseline.
- Eureka and Dominium target-pilot evidence remains target-repo evidence and is
  not a broad product-readiness claim.
- Exact tokenizer/provider billing, live provider/model execution, branch
  workflow helpers, and CI enforcement remain future work.

## Work Item: Q25 Pack Provenance Revalidation

### Status

Implemented as a Q25 fix-forward and awaiting Q25 review with the rest of the
repair packet.

### Changed Paths

- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_export_import.py`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/queue/Q25-importer-scope-and-state-truth-repair/evidence/**`
- `docs/reference/cross-repo-pack-export-import.md`

### Rationale

Repeated Q25 validation confirmed that checksum validation was coherent, but
`pack-status` still needed an explicit provenance guard. A stale clean
`manifest.yaml` must fail instead of being accepted merely because mutable
metadata is excluded from payload checksums.

### Implementation Notes

- Added manifest scalar parsing and pack provenance validation to AIDE Lite.
- Included provenance status in `validate` and `pack-status`.
- Treated explicit dirty-source provenance as reportable and non-failing while
  failing stale clean provenance, missing fields, and malformed dirty-state
  values.
- Regenerated the export pack so target imports receive the hardened checker.
- Recorded the new convention in Q25 evidence and the cross-repo import
  reference.

### Verification

Targeted export/import tests, full `.aide/scripts/tests` discovery, AIDE Lite
validate/test/pack-status, Harness validate/doctor/self-check, Harness,
Compatibility, Gateway, and Provider unit suites, regenerated safe-import
fixture smoke, diff check, ignore checks, and targeted secret scans passed.
