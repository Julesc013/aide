# Repository Layout

## Purpose

This reference records the current AIDE repository layout contract created by
`AIDE-STRUCTURE-01-root-authority-contracts`. It is a planning and reference
surface for future Track B work.

The authoritative machine-readable policy is
`.aide/policies/root-authority.yaml`.

## Closed Root Model

The current tracked root model is closed to these roots:

- `.aide`
- `.aide.local.example`
- `.agents`
- `.codex`
- `bridges`
- `core`
- `docs`
- `environments`
- `evals`
- `fixtures`
- `governance`
- `hosts`
- `inventory`
- `labs`
- `matrices`
- `packaging`
- `platforms`
- `research`
- `scripts`
- `shared`
- `specs`

Generated reports may also refer to `repo-root` as an inventory concept. It is
not a directory to expand.

New top-level roots are not allowed for symmetry. `tools`, `tests`, `examples`,
and `archive` are add-only candidates that need separate reviewed queue
authority.

## Authority Map

| Root | Authority | Current posture |
| --- | --- | --- |
| `.aide` | Repo-local contract, queue, policies, protocol schemas, evidence, reports, OKF projections, and control-plane status | Mixed; queue-scoped mutation only |
| `.aide.local.example` | Template-only local runtime-state example | Preserve template |
| `.agents` | External agent/tool interop guidance and generated projections | Needs dot-tool interop policy |
| `.codex` | Codex/tool interop projection only | Needs dot-tool interop policy |
| `core` | Reusable implementation library | Implementation tasks only |
| `governance` | Human-readable repository law and doctrine | Review required for law changes |
| `docs` | Human documentation, references, operations, planning, decisions, roadmap explanations | Docs-normalization tasks |
| `inventory` | Observed exact facts and records | Inventory tasks |
| `matrices` | Cross-cutting support, capability, conformance, verification, host, bridge, risk, and release views | Matrix tasks |
| `hosts` | IDE and host integrations or host-lane proofs | Host tasks only |
| `bridges` | Target-repo bridge metadata and adoption expectations | Bridge tasks only |
| `scripts` | Stable command wrappers | Wrapper tasks only |
| `shared` | Bootstrap-era shared implementation and tests pending fate mapping | Fate map required |
| `platforms` | Candidate for split across hosts, environments, inventory, matrices, and docs | Fate map required |
| `research` | Candidate human research input or compiled OKF/reference input | Fate map required |
| `specs` | Bootstrap-era human and implementation-facing specifications pending authority split | Fate map required |
| `environments` | Environment and execution-topology records | Environment/lab tasks |
| `evals` | Evaluation definitions, runs, and golden checks | Eval tasks |
| `fixtures` | Canonical deterministic input and output fixtures | Narrow fixture authority required |
| `packaging` | Source packaging shape and release-bundle templates | Packaging tasks only |
| `labs` | Prototypes only | Promotion requires queue review |

## Overlap Report

Current known overlaps:

- `.aide` contains both canonical records and generated evidence. The
  distinction is by subtree and policy, not by root name alone.
- `core` implements protocol helpers, while `.aide/protocol` owns schema files.
  Neither should silently replace the other.
- `governance` and `.aide/policies` both describe law. Governance is human
  doctrine; `.aide/policies` is machine-readable policy.
- `docs` and OKF pages both explain state. Neither overrides queue, protocol,
  policy, or evidence truth.
- `inventory` and `matrices` both summarize facts. Matrices are views and must
  stay backed by inventory, queue, evidence, or policy records.
- `hosts`, `bridges`, and `platforms` overlap around host and target-repo
  concepts. `platforms` needs a fate map before movement.
- `shared`, `specs`, and `core` overlap around bootstrap-era implementation and
  architecture. They need a fate map before any extraction or consolidation.
- `.agents` and `.codex` overlap with generated adapter guidance. They need a
  dot-tool interop policy before expansion.

## Candidate Target Structure

Near-term structural direction is additive and contract-first:

```text
.aide/
  protocol/
  policies/
  queue/
  reports/
  knowledge/okf/
  context/
  intake/

core/
  protocol/
  knowledge/
  reconciler/
  conformance/    # add only when ConformanceProfile work needs it
  patching/       # add only when PatchTransaction work needs it
  adapters/       # add only when AdapterManifest or adapter port work needs it
  context/        # add only when ContextPack work needs it
  interop/        # add only when interop export or MCP/A2A contract work needs it
  runtime/        # deferred until runtime is explicitly authorized

governance/
docs/
inventory/
matrices/
hosts/
bridges/
scripts/
fixtures/
environments/
evals/
packaging/
labs/
shared/           # fate map required before movement
platforms/        # fate map required before movement
research/         # fate map required before movement
specs/            # fate map required before movement
```

Do not create empty roots or packages merely to match this sketch.

## Migration Rules

Future migration tasks must:

1. Start from live `.aide/queue/` truth.
2. Refresh repo intelligence, root recycling, and refactor map evidence.
3. Produce a no-apply move/salvage/reference plan before any apply-capable work.
4. Preserve bootstrap-era history unless a reviewed task records a narrower
   archival decision.
5. Treat generated outputs as evidence or projections unless policy explicitly
   says otherwise.
6. Keep target-repo truth separate from AIDE-source generated reports.
7. Stop at review gates for source-of-truth changes, migration behavior,
   destructive operations, branch mutation, release work, and permission
   widening.

## Validation Plan

For future structure work, run the strongest relevant subset of:

```powershell
git status --short --branch
py -3 .aide/scripts/aide_lite.py doctor
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py repo inventory
py -3 .aide/scripts/aide_lite.py repo status
py -3 .aide/scripts/aide_lite.py repo validate
py -3 .aide/scripts/aide_lite.py roots inventory
py -3 .aide/scripts/aide_lite.py roots classify
py -3 .aide/scripts/aide_lite.py roots plan
py -3 .aide/scripts/aide_lite.py roots validate
py -3 .aide/scripts/aide_lite.py refactor map
py -3 .aide/scripts/aide_lite.py refactor validate-map
py -3 .aide/scripts/aide_lite.py task inspect --task-id <TASK-ID>
py -3 .aide/scripts/aide_lite.py task evidence --task-id <TASK-ID>
git diff --check
```

Use broader validation when a task changes shared policy, root contracts,
protocol records, migration maps, or generated output boundaries.

## Follow-Up Prompts

Track B continues with:

1. `AIDE-STRUCTURE-02-status-doc-sync`
2. `AIDE-STRUCTURE-03-shared-platforms-research-specs-fate-map`
3. `AIDE-STRUCTURE-04-dot-tool-roots-interop-policy`
4. `AIDE-STRUCTURE-05-tools-tests-examples-root-plan`

Prompt shells are recorded in
`docs/planning/repository-structure/track-b-follow-up-prompts.md`.
