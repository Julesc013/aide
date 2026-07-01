# AIDE Full Synthesis Report And Best Plan

## Status

ADVISORY_SYNTHESIS_REAPPLIED_AFTER_ORIGIN_SYNC.

## Post-Sync Note

This report was first authored before local `main` was fast-forwarded from
`origin/main` on July 2, 2026. It has been reapplied after that sync as
historical advisory synthesis, not as current queue truth.

The synced upstream history already contains several pieces this report had
identified as future or candidate work, including:

- a read-only More Infinite Research canary-profile lane;
- distribution-product status and package/shadow canary planning;
- a Project Intelligence planning spine under
  `docs/planning/project-intelligence-spine.md`;
- queue records for ProjectGraph, naming authority, ContextPack v2,
  Workbench-view planning, and related self-management work.

The current latest task packet after sync names
`AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01`, not Q49. Therefore Q49-era statements
below should be read as the original synthesis context and warning history,
not as the active next-task selector. Current execution must follow
`.aide/context/latest-task-packet.md`, `.aide/queue/index.yaml`, and current
validation output.

This report answers the operator request for a full synthesis of the pasted
advisory documents plus current AIDE docs, code-facing command surfaces,
generated reports, queue state, validation evidence, and repository blockers.

The original synthesis prompt was compiled through AIDE intake. The compiler
classified it as `release` risk, `blocked`, and `safe_to_execute: false`, with
the next action to write a blocker/advisory report and require reviewed
authorization before mutation. This report therefore does not accept a roadmap,
create queue items, mutate target repositories, publish releases, call
providers or models, create branches, push, tag, or claim readiness.

## Executive Synthesis

AIDE is already strong at one thing: deterministic, local, evidence-rich,
report-first governance. It can inventory the repo, classify ownership,
generate compact context, validate evidence, draft release text locally,
package a portable AIDE Lite pack, plan installs/upgrades/rollback/uninstall
without applying them, and preserve no-call/no-apply boundaries.

AIDE is not yet an autonomous development runtime, not an apply-capable target
installer, not a public release, not a live provider gateway, and not a broad
product surface. The best plan should lean into the strength that exists:

```text
truth-first reports
-> read-only real canaries
-> graph-backed project intelligence
-> work-product conservation
-> transaction-backed changes
-> reviewed target apply
-> publication only after target proof
```

The pasted documents are directionally correct but incomplete unless merged
with live repo truth. Their strongest combined idea is:

```text
AIDE should adopt real projects through read-only canaries, understand them
through ProjectGraph, conserve their work products through explicit lifecycle
records, and change them only through evidence-backed transactions.
```

That is better than treating AIDE as either a directory cleanup tool, a release
bundle generator, or an automatic editor. It gives AIDE a path from governance
substrate toward useful self-hosted engineering without jumping trust gates.

## Current Truth From The Repo

### Product And Lifecycle

- AIDE is `reboot/pre-product` in `.aide/profile.yaml`.
- The repository is an in-place reboot, not a restart.
- The accepted public model remains AIDE Core, AIDE Hosts, and AIDE Bridges.
- Runtime, SDK, product hosts, Service, Commander, Mobile, provider calls, and
  live routing remain not implemented or deferred.

### Implemented Substrate

The root docs and reference docs show a broad implemented substrate:

- Profile/Contract v0 and filesystem queue.
- Harness v0 and AIDE Lite command surfaces.
- Generated-artifact boundaries.
- Compatibility baseline and Dominium Bridge baseline.
- Token survival, context compiler, verifier, review packets, token ledger,
  golden tasks, outcome controller, route decisions, cache/local-state boundary.
- Local/report-only Gateway skeleton and offline provider metadata.
- Cross-repo export/import pack.
- Existing-tool adapter compiler.
- Commit discipline, changelog previews, WorkUnit recovery, Git workflow, and
  dry-run helper plans.
- Intent compiler and prompt normalization.
- Repo intelligence and file quality ledgers.
- Refactor, roots, tools, install, repair, upgrade, rollback, uninstall,
  release bundle, and GitHub Release draft surfaces.

These are mostly report-first or dry-run-first. That is not weakness; it is the
trust foundation.

### Original Queue And Phase State

At original authoring time, the docs said Q48 local GitHub Release draft
generation was implemented for review. The latest task packet said Q49
Dominium Fresh Install Preflight was next. QCHECK-04 said Q49 could proceed
with warnings from the local bundle and safe import/preflight path.

However, original live inspection found a critical mismatch:

- `.aide/context/latest-task-packet.md` says Q49.
- `py -3 .aide/scripts/aide_lite.py task inspect` reports Q49 task surfaces
  are missing.
- `.aide/context/latest-context-packet.md` still reports current queue as
  `.aide/queue/Q17-router-profile-v0/`.
- `.aide/profile.yaml` still says current focus is Q31.

After the origin sync, that specific Q49-next framing is no longer the active
task context. The broader lesson remains valid: AIDE's latest packets, profile
records, generated reports, and queue index must agree before new accepted work
is added.

### Original Validation And Readiness

The original broad validation picture was mixed:

- `intent validate`: PASS.
- `git diff --check`: PASS after the advisory changes.
- `doctor`: FAIL because broad validation is failing.
- `validate`: FAIL on export pack checksum drift in
  `.aide/export/aide-lite-pack-v0/files/.aide.local.example/**`.
- QCHECK-04 previously recorded `PASS_WITH_WARNINGS` and supported Q49 with
  warnings, but current live validation must outrank older checkpoint comfort.

No public release, remote handoff, target install, or product readiness claim
should be made from this report. Current validation must be rerun against the
post-sync checkout before any readiness or release-shaped claim.

### Repo Intelligence And Quality

The generated repo intelligence reports:

- 1543 tracked files in the latest repo-intelligence snapshot.
- 313 docs, 500 evidence files, 324 generated files, 37 source files, 35 tests,
  43 policies, 109 fixtures, and 146 unknown files.
- 277 unknown-owner files.
- 451 orphan candidates.
- 9335 stale doc-link candidates.

The file quality report adds:

- 1589 quality records.
- 1242 warnings.
- 718 stale doc reference candidates.
- 274 reuse candidates.
- 63 missing-doc candidates.
- 42 missing-test-or-validator candidates.
- 146 unknown kind/status candidates.
- 277 unknown-owner candidates.
- No tracked local-state or secret-path failures.

These are candidate signals, not deletion or refactor authority. They show that
AIDE has enough eyes to plan smarter work, but not enough semantic intelligence
to safely mutate structure automatically.

### Code Surface

The main executable implementation surface is `.aide/scripts/aide_lite.py`.
It is currently about 779 KB and exposes a very wide command tree:

```text
doctor, validate, estimate, snapshot, index, context, map, pack, verify,
review-pack, ledger, eval, commit, changelog, github, intent, repo, quality,
refactor, roots, tools, install, repair, upgrade, rollback, uninstall, release,
task, git, outcome, optimize, route, cache, gateway, provider, export-pack,
import-pack, pack-status, adapter, adapt, selftest, test, version, show-config
```

The quality report marks `.aide/scripts/aide_lite.py` as a large,
mixed-purpose, missing-doc, public-surface, reuse-candidate module. That does
not mean it should be split now. It means future code work should first build a
ProjectGraph/SymbolIndex and a transaction-backed extraction plan. A direct
refactor of this file before graph-level context would be reckless.

The reuse report also shows repeated helper names across host proof lanes,
tests, gateway/provider utilities, and AIDE Lite. Some repetition is expected
in proof lanes and fixtures. Some may become reusable helpers later. None of
it is proof of duplication safe to remove.

## Synthesis Of The Three Pasted Advisory Documents

### 1. MIR As First Practical Canary

The MIR handoff argues that `julesc013/more-infinite-research` should be the
first practical downstream canary instead of ScreenSave. That is a good
operator-priority shift if the goal is fast useful feedback:

- MIR is likely smaller than ScreenSave.
- It has a concrete product format: Factorio mod metadata, Lua files, locale,
  settings, prototypes, and release artifacts.
- It can expose source-versus-release drift, validation-profile gaps, package
  checks, and update workflow needs.
- It is useful without requiring AIDE to mutate targets on day one.

The correct MIR first step is not "AIDE edits the mod." It is:

```text
AIDE-BUILD-CANARY-PROFILE-MORE-INFINITE-RESEARCH-01
```

with read-only scope:

- target identity
- local/public availability
- repo cleanliness if local
- Factorio metadata if available
- file-role classification
- ownership and protected paths
- validation surfaces
- release/source drift
- blockers to shadow apply
- blockers to real apply
- explicit non-capabilities

The MIR public facts in the pasted handoff were not reverified here. A reviewed
MIR canary task must verify them against local or public target state before
recording them as current truth.

### 2. ProjectGraph As Missing Intelligence

The ProjectGraph handoff is the deepest architectural improvement. AIDE should
not stop at repository structure. It should model physical and semantic
project structure:

- paths, files, roots, generated outputs, reports
- modules, symbols, imports, calls, references
- docs, comments, claims, links
- tests, fixtures, assertions
- issues, bugs, WorkUnits, evidence
- purpose, contracts, ownership, usage
- performance observations and complexity findings
- change events and transactions

This is the right center of gravity. AIDE already has Q37/Q38 deterministic
file and quality layers. The next leap is to turn those into a graph model,
starting report-only.

The first ProjectGraph should be intentionally small:

```text
ProjectGraphSnapshot v0:
  path nodes
  file nodes
  doc nodes
  report nodes
  generated artifact nodes
  evidence nodes
  WorkUnit nodes
  test/fixture nodes
  owner/status/kind edges
  references/docs/tests/generates/consumes edges
```

Then add symbol and claim layers:

```text
SymbolIndex v0
DocCodeClaimLinker v0
PurposeLedger v0
ContractRecord v0
UsageRecord v0
ReuseOpportunityFinding v0
```

None of these should apply refactors. The goal is "eyes before hands."

### 3. Work Product Conservation As Missing Lifecycle

The work-conservation handoff supplies the missing lifecycle law:

```text
No useful work disappears without a recorded disposition.
No reusable work remains invisible.
No failed work teaches nothing.
No task closes without harvest evidence.
```

AIDE already produces many scripts, fixtures, reports, test helpers, evidence
files, generated artifacts, prompts, and failure lessons. Some are canonical,
some are task-local, and some are stranded. The next improvement is a
WorkProductLedger and TaskHarvest report:

```text
WorkProductRecord:
  artifact/path
  kind
  purpose
  owner
  source WorkUnit
  evidence refs
  lifecycle state
  reuse class
  disposition
  blockers
```

Start report-only. Do not promote scripts or tests automatically. Promotion
requires transaction support and review.

## The Original Best Plan

The original best plan had eight layers. After the origin sync, some layers are
already represented in upstream queue records, so this section should be used
as synthesis context rather than as an execution order.

### Layer 0: Stop And Classify Current Dirty State

Goal: avoid building on unclear local state.

Actions:

- Classify the current dirty tree:
  - generated intake packets
  - generated Git helper plan outputs
  - advisory reports
- Do not stage, commit, push, or sync without explicit operator approval.
- Keep `main...origin/main [behind 263]` visible as a branch-state warning.
- Avoid `pack --task` unless intentionally refreshing latest task context,
  because it rewrites `.aide/context/latest-task-packet.md`.

Exit criteria:

- Dirty changes are either intentionally preserved as advisory evidence or
  separately committed under AIDE commit discipline after approval.

### Layer 1: Truth-Surface Freshness Repair

Goal: make AIDE agree with itself before adding new ambitions.

Candidate WorkUnit:

```text
AIDE-RECONCILE-TRUTH-SURFACES-Q49-01
```

Scope:

- `.aide/profile.yaml`
- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-task-packet.md`
- `.aide/queue/index.yaml`
- Q49 task-surface records if authorized
- root docs only if they are stale relative to queue truth

Questions to answer:

- Is Q49 truly the current next task?
- Should a Q49 queue directory/task/status/evidence surface exist now?
- Is `.aide/profile.yaml` current focus stale and safe to update?
- Is `latest-context-packet.md` stale because it was not regenerated?
- Which generated outputs should be refreshed, and which should be left as
  historical evidence?

Non-goals:

- no target mutation
- no pack release
- no publication
- no branch mutation
- no runtime/provider work

Exit criteria:

- task inspect no longer contradicts latest task packet, or the contradiction
  is recorded as a deliberate blocker.
- profile/current-focus and context surfaces are either updated or explicitly
  marked stale/preserved.

### Layer 2: Validation And Export Pack Checksum Repair

Goal: restore the broad validation base before using release-shaped artifacts.

Candidate WorkUnit:

```text
AIDE-REPAIR-EXPORT-PACK-CHECKSUM-DRIFT-01
```

Scope:

- export pack checksum evidence
- `.aide.local.example/**` export-pack entries if drift is confirmed
- validation evidence
- no release publication

Evidence to collect:

- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py pack-status`
- `py -3 .aide/scripts/aide_lite.py release validate`
- `py -3 .aide/scripts/aide_lite.py release draft-validate`
- `git diff --check`

Exit criteria:

- broad validation either passes or has a narrow classified failure.
- export pack checksum mismatches are resolved or explicitly blocked.

### Layer 3: Q49 Dominium Fresh Install Preflight

Goal: execute the already-indicated local next phase, but only after Q49 task
surfaces and validation state are coherent.

Candidate WorkUnit:

```text
Q49-dominium-fresh-install-preflight
```

Scope:

- target preflight only
- safe import/preflight path
- preserve target memory, queue, evidence, golden tasks, doctrine, tools, and
  manual `AGENTS.md` content
- no install apply beyond reviewed preflight behavior
- no publication
- no branch mutation

Why it still matters:

Q49 is the local release-bundle reality check. AIDE should not claim install
readiness from Q47/Q48 source artifacts alone.

Exit criteria:

- Dominium target preflight evidence exists.
- No target product mutation beyond authorized preflight artifacts.
- Remaining target blockers are explicit.

### Layer 4: MIR Read-Only Canary Profile

Goal: add immediate practical value without target mutation.

Candidate WorkUnit:

```text
AIDE-BUILD-CANARY-PROFILE-MORE-INFINITE-RESEARCH-01
```

Scope:

- read-only local/public target inspection
- Factorio mod metadata profile
- file-role classification
- ownership/protected paths
- validation commands and dependencies
- source-versus-release drift
- blockers to shadow apply, real apply, and release

Outputs:

- `.aide/reports/canary-profiles/more-infinite-research-v0/current.json`
- `.aide/reports/canary-profiles/more-infinite-research-v0/current.md`
- task-local evidence

Non-goals:

- no MIR mutation
- no branch/worktree automation
- no package generation unless separately authorized
- no mod portal upload
- no GitHub Release publication
- no provider/model calls

Exit criteria:

- MIR canary profile exists as report-only evidence.
- recommended next MIR validation task is explicit.

### Layer 5: MIR Validation And Update Context

Goal: turn MIR from a known target into a useful engineering workflow.

Candidate WorkUnits:

```text
AIDE-BUILD-MIR-VALIDATION-PROFILE-V0-01
AIDE-BUILD-MIR-UPDATE-CONTEXT-PACK-V0-01
AIDE-BUILD-MIR-SHADOW-UPDATE-CANARY-V0-01
```

Validation ideas:

- `info.json` parse and schema sanity
- version format and release/source comparison
- required Factorio files present
- Lua syntax check if local Lua runner exists
- locale key coverage
- settings/defaults consistency
- prototype-generation sanity
- package zip dry-run only after authorization

Exit criteria:

- MIR has a reusable validation profile.
- human/Codex update work can start from bounded context.
- shadow apply remains temp-only and review-gated.

### Layer 6: ProjectGraph Foundation

Goal: make AIDE understand projects semantically before changing them.

Candidate WorkUnits:

```text
AIDE-BUILD-PROJECT-GRAPH-SNAPSHOT-V0-01
AIDE-BUILD-SYMBOL-INDEX-V0-01
AIDE-BUILD-DOC-CODE-CLAIM-LINKER-V0-01
AIDE-BUILD-PURPOSE-LEDGER-V0-01
AIDE-BUILD-REUSE-OPPORTUNITY-REPORTS-V0-01
```

Implementation posture:

- report-only
- no refactor
- no deletion
- no path movement
- no reference rewrite
- no target mutation

Why now:

Q37/Q38 already produce file inventory, ownership, dependency, test, docs, and
quality evidence. ProjectGraph is the natural next unifier.

Exit criteria:

- ContextPack v2 can include graph slices, not just file refs.
- future refactors can cite affected symbols/docs/tests/reports/evidence.

### Layer 7: Work Product Conservation

Goal: stop useful work from disappearing or staying stranded.

Candidate WorkUnits:

```text
AIDE-BUILD-WORK-PRODUCT-LEDGER-V0-01
AIDE-BUILD-TASK-HARVEST-REPORTS-V0-01
AIDE-BUILD-REUSE-REGISTRY-V0-01
AIDE-BUILD-TEST-ASSET-CATALOG-V0-01
AIDE-BUILD-SCRIPT-LIFECYCLE-LEDGER-V0-01
AIDE-BUILD-FIXTURE-CATALOG-V0-01
```

Initial dispositions:

- task_local_evidence
- candidate_reusable
- promoted_reusable
- accepted_canonical
- generated_projection
- fixture
- test_asset
- tool
- documentation
- knowledge_observation
- deprecated
- superseded
- archived
- quarantined
- discarded_with_reason

Exit criteria:

- task outputs can be harvested without promoting anything automatically.
- stranded scripts/tests/fixtures/docs become visible.
- failures can become negative fixtures or regression tests.

### Layer 8: Transaction-Backed Change

Goal: create the first safe path from report evidence to actual mutation.

Candidate WorkUnits:

```text
AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01
AIDE-BUILD-STRUCTURE-TRANSACTION-SCHEMA-01
AIDE-BUILD-CODE-STRUCTURE-TRANSACTION-SCHEMA-01
AIDE-BUILD-DOC-STRUCTURE-TRANSACTION-SCHEMA-01
AIDE-BUILD-REFERENCE-REWRITE-PLAN-SCHEMA-01
AIDE-BUILD-WORK-PRODUCT-PROMOTION-TRANSACTION-V0-01
```

Required inputs:

- ProjectGraph slice
- WorkProduct records
- allowed/forbidden paths
- ownership evidence
- affected docs/tests/reports/symbols
- validation plan
- rollback plan
- human review decision

Exit criteria:

- mutation is previewable, reversible, evidence-backed, and review-gated.

## What Not To Do

Do not:

- jump from MIR idea to real MIR mutation
- edit ScreenSave or MIR from the AIDE source repo without target-local
  authority
- publish the AIDE Lite pack
- create tags or GitHub Releases
- push or sync `main`
- create `dev`
- call provider/model/network services
- start Runtime, Service, Commander, Mobile, MCP/A2A, Workbench, or app surface
  work ahead of queue authority
- refactor `.aide/scripts/aide_lite.py` before graph-backed planning
- treat stale doc-link/orphan/reuse candidates as deletion or move authority
- treat generated source-repo reports as target truth

## What Is Better Than The Pasted Plan

The pasted plan is good, but the improved version adds five corrections:

1. Put live truth repair before all new roadmap ambition.
2. Treat MIR as first read-only practical canary, not an immediate edit target.
3. Make ProjectGraph the umbrella for repo intelligence, code intelligence,
   doc truth, usage, tests, issues, evidence, performance, and transactions.
4. Make work conservation a harvest gate with explicit dispositions.
5. Use transactions as the bridge from evidence to mutation.

The strongest product sentence is:

```text
AIDE is a preservation-first engineering control plane that learns real
projects by observing them, explains them through graph-backed knowledge,
conserves development value, and mutates only through reviewed transactions.
```

## Immediate Recommended Next Prompt

If the operator wants the safest next concrete work, use:

```text
Create and process AIDE-RECONCILE-TRUTH-SURFACES-Q49-01.

Repo truth outranks this prompt.

Goal:
Reconcile current AIDE truth surfaces before any new canary, release, target
install, or roadmap mutation.

Scope:
- inspect `.aide/context/latest-task-packet.md`
- inspect `.aide/context/latest-context-packet.md`
- inspect `.aide/profile.yaml`
- inspect `.aide/queue/index.yaml`
- inspect whether Q49 task surfaces exist
- inspect current validation and export-pack checksum drift
- produce a blocker or repair plan

Allowed paths:
- `.aide/intake/**`
- `.aide/reports/**` for advisory evidence
- `.aide/context/**` only if explicitly regenerating context is authorized
- root docs only if they are stale relative to current queue truth

Forbidden:
- no target repo mutation
- no release publication
- no GitHub API
- no branch mutation
- no provider/model/network calls
- no runtime/provider/gateway/app/host implementation

Validation:
- `git status --short --branch`
- `py -3 .aide/scripts/aide_lite.py task inspect`
- `py -3 .aide/scripts/aide_lite.py intent validate`
- `py -3 .aide/scripts/aide_lite.py validate`
- `git diff --check`

Expected result:
PASS_WITH_WARNINGS, BLOCKED, or NEEDS_REVIEW.
```

If the operator wants visible practical value next, use the MIR canary prompt
after truth-surface reconciliation:

```text
Create and process AIDE-BUILD-CANARY-PROFILE-MORE-INFINITE-RESEARCH-01 as a
read-only downstream canary profile. No MIR mutation, no apply, no release, no
push, no branch automation, no provider/model calls, and no unverified readiness
claims.
```

## Final Verdict

The original best plan was not "more docs," "more release draft," or "start
runtime." It was:

```text
repair truth freshness
-> restore validation
-> run Q49 preflight
-> adopt MIR read-only
-> build MIR validation context
-> build ProjectGraph
-> add work-product harvest
-> introduce transaction-backed mutation
-> only then apply, package, or publish
```

After the origin sync, the current best plan is to preserve the live queue's
newer Project Intelligence, MIR, distribution, and self-management progress;
use this report as advisory background; and make any roadmap/TODO edits in a
fresh reviewed planning pass grounded in the synced queue state.

That gives AIDE a real path from disciplined evidence machinery to useful
engineering agency without breaking its own trust model.
