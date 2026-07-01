# AIDE Advisory Intake Report: MIR Canary, ProjectGraph, And Work Conservation

## Status

BLOCKED_FOR_DIRECT_EXECUTION_REAPPLIED_AFTER_ORIGIN_SYNC.

## Post-Sync Note

This report was first authored before local `main` was fast-forwarded to
`origin/main` on July 2, 2026. It has been reapplied after that sync as
historical advisory intake evidence.

The synced upstream history already contains newer MIR, distribution,
Project Intelligence, and self-management queue work. Current execution must
therefore follow `.aide/context/latest-task-packet.md`, `.aide/queue/index.yaml`,
and current validation output rather than the Q49-era next-task framing below.

This report documents an operator-requested assessment of three pasted advisory
handoffs:

- Use `julesc013/more-infinite-research` as the first practical downstream
  canary before ScreenSave.
- Expand AIDE from repository structure intelligence to ProjectGraph-level
  project intelligence.
- Add work-product conservation so useful scripts, tests, fixtures, reports,
  failed attempts, and notes receive explicit fates.

The AIDE intent compiler classified the original raw request as blocked for direct
execution. This report is therefore advisory evidence only. It does not mutate
the queue, accept a roadmap, change release posture, update target repositories,
publish artifacts, call providers, call live models, or verify public MIR
metadata over the network.

## Original Local Repo Preflight

- Original branch snapshot: `main...origin/main [behind 263]`.
- Original latest task packet: `Q49 - Dominium Fresh Install Preflight`.
- Original `task inspect` result: Q49 task surfaces are missing.
- `intent compile` result: PASS, but direct execution is blocked.
- `intent validate` result: PASS.
- `doctor` result: FAIL because validation is required/failing.
- `validate` result: FAIL due export pack checksum drift in
  `.aide/export/aide-lite-pack-v0/files/.aide.local.example/**`.

These findings meant the pasted sequences were not current canonical queue
truth at original authoring time. After the origin sync, the specific Q49
framing is superseded by newer queue state, but the boundary still holds:
advisory synthesis must not outrank live queue truth.

## Assessment

The handoffs are directionally strong, but they are not yet the best complete
plan if left as three independent ideas.

The stronger plan is to combine them into one layered posture:

```text
current queue truth and validation health
-> read-only MIR canary profile
-> MIR validation/context profile
-> ProjectGraph report-only intelligence
-> work-product ledger and harvest gate
-> transaction-backed promotion or target update
```

That order matters. MIR gives AIDE a small, real, useful downstream target.
ProjectGraph gives AIDE the semantic context needed before broad mutation.
Work-product conservation prevents reusable effort from being buried in task
folders. But none of those should skip the current queue gate or validation
blockers.

## Answer To "Is This The Best We Can Do?"

No. It is the best shape of the idea so far, but it can be better in three
ways.

First, decouple the strategic recommendation from stale queue ids. The pasted
handoffs mention several next-task names that do not match the local latest
packet. The durable decision should be:

```text
After the current reviewed gate is reconciled, prefer MIR as the first practical
downstream canary unless the operator explicitly chooses another target.
```

Second, make ProjectGraph the umbrella concept instead of adding isolated
ledgers. Repo intelligence, file quality, refactor planning, root recycling,
tool absorption, install, repair, upgrade, rollback, release, and future code
intelligence should all become slices of one project graph. The first graph
should be report-only.

Third, make work conservation a lifecycle gate, not a cleanup wish. Every
meaningful task output should have a recorded purpose, owner, evidence link,
reuse class, lifecycle state, and disposition. Nothing should be promoted,
moved, deleted, or archived without preview and review.

## Recommended Better Sequence

1. Reconcile live AIDE state before adding new roadmap truth.
   - Resolve the active latest-packet versus task-surface mismatch, if any.
   - Refresh or repair export pack checksum evidence.
   - Keep the repo behind-origin state visible; do not use remote truth without
     explicit sync work.

2. Add MIR only as a reviewed read-only canary candidate.
   - Candidate id: `AIDE-BUILD-CANARY-PROFILE-MORE-INFINITE-RESEARCH-01`.
   - Scope: inventory, ownership, validation surface, release/source drift,
     and non-capabilities.
   - Non-goals: no MIR mutation, no apply, no branch automation, no release,
     no publish, no provider/model calls.

3. Build MIR validation and context only after the profile exists.
   - Candidate id: `AIDE-BUILD-MIR-VALIDATION-PROFILE-V0-01`.
   - Include `info.json` parsing, required Factorio mod files, Lua syntax if a
     local Lua runner exists, locale checks, settings/defaults consistency,
     package dry-run only if later authorized, and source/release version drift.

4. Add ProjectGraph as the intelligence foundation.
   - Candidate id: `AIDE-BUILD-PROJECT-GRAPH-SNAPSHOT-V0-01`.
   - Initial nodes: paths, files, docs, reports, generated artifacts, tests,
     fixtures, WorkUnits, evidence, and known ownership records.
   - Later nodes: sections, symbols, imports, calls, doc claims, issues,
     bugs, performance observations, purpose records, contracts, and usage.
   - Start report-only, with no automatic refactor.

5. Add work-product conservation as a separate report-only lane.
   - Candidate id: `AIDE-BUILD-WORK-PRODUCT-LEDGER-V0-01`.
   - Candidate id: `AIDE-BUILD-TASK-HARVEST-REPORTS-V0-01`.
   - Classify task-local scripts, tests, fixtures, reports, prompts, failed
     attempts, and docs as reusable, evidence-only, generated, archived,
     superseded, quarantined, or discarded-with-reason.

6. Only then introduce transaction-backed mutation.
   - Patch, code-structure, doc-structure, reference-rewrite, promotion, and
     target-update work should consume ProjectGraph and WorkProduct evidence.
   - Real downstream apply, branch mutation, packaging, and release publication
     remain future reviewed work.

## MIR Judgment

MIR is a better first practical downstream canary than ScreenSave if the goal is
near-term visible usefulness. It appears smaller, more focused, and easier to
inventory as a Factorio Lua mod. It is also useful because release/source
metadata drift is exactly the kind of practical issue AIDE should detect.

However, the MIR facts in the pasted handoff were not reverified live during
this intake. Treat claims such as current version, latest release, dependencies,
and file layout as advisory input until a reviewed canary task verifies local or
public target state.

ScreenSave should not be erased from the larger productization story. It is a
heavier downstream canary. MIR is simply the better first canary for a small,
real, fast feedback loop.

## ProjectGraph Judgment

ProjectGraph is the right center of gravity.

AIDE should not only know where files live. It should know what project objects
mean, why they exist, who uses them, what tests or docs cover them, what claims
depend on them, what work changed them, and what would break if they moved.

The near-term implementation should be deliberately modest:

```text
ProjectGraphSnapshot v0
SymbolIndex v0
DocCodeClaimLinker v0
PurposeLedger v0
ReuseOpportunityReports v0
```

Each begins as a report. No refactor, rename, deletion, migration, or repair is
authorized by the presence of a graph finding.

## Work Conservation Judgment

Work-product conservation is the missing lifecycle rule.

AIDE should preserve development value without hoarding active clutter. The rule
should be:

```text
No useful work disappears without a recorded disposition.
No reusable work remains invisible.
No failed work teaches nothing.
No task closes without harvest evidence.
```

The first useful shape is a report-only WorkProductLedger and harvest report,
not an automatic promotion command. Promotion of scripts, tests, fixtures, docs,
or examples should wait for transaction support and review.

## Better Product Principle

The compact principle is:

```text
AIDE should adopt real projects through read-only canaries, reason about them
through ProjectGraph, conserve their work products through explicit lifecycle
records, and change them only through evidence-backed transactions.
```

That is stronger than a directory cleanup plan, stronger than an isolated MIR
pivot, and safer than immediate target apply.

## Blockers

- The latest local task packet names Q49, but `task inspect` reports missing
  Q49 task surfaces.
- Broad validation currently fails on export pack checksum drift.
- The repository branch is behind `origin/main` by 263 commits.
- The pasted current-task ids do not match local queue truth and must not be
  executed as if current.
- MIR public metadata was not reverified in this intake.

## Deferrals

- No `docs/roadmap/**` updates.
- No `DOCUMENTATION.md` index update.
- No queue item creation.
- No target repository inspection or mutation.
- No network verification of MIR public facts.
- No `pack --task` run, to avoid overwriting the canonical Q49 latest task
  packet for this advisory intake.
- No commit.

## Original Recommended Next Reviewed Work

The next reviewed action should be one of:

```text
AIDE-RECONCILE-Q49-TASK-SURFACES-01
AIDE-BUILD-CANARY-PROFILE-MORE-INFINITE-RESEARCH-01
AIDE-BUILD-PROJECT-GRAPH-SNAPSHOT-V0-01
AIDE-BUILD-WORK-PRODUCT-LEDGER-V0-01
```

After the origin sync, MIR canary-profile work already exists in the upstream
queue as read-only/partial public-metadata work. The next planning pass should
compare this report against the synced MIR and Project Intelligence queue
records before adding or editing roadmap/TODO material.
