# AIDE Planning Index

## Purpose

`PLANS.md` is the repository's working plan index for substantial engineering work. It exists to track real execution intent, dependencies, milestones, blockers, and verification plans. It is not a marketing roadmap.

## How Plans Are Structured

- Each substantial work item should have a stable identifier such as `P00`, `P01`, or a later program-specific id.
- A plan entry should describe one coherent objective.
- Plans should be updated as work progresses rather than rewritten after the fact.
- Status values should be explicit, for example `proposed`, `active`, `blocked`, `completed`, or `superseded`.

## Recommended Fields For A Plan Entry

- `Plan ID`
- `Title`
- `Status`
- `Objective`
- `Scope`
- `Allowed Paths`
- `Dependencies`
- `Milestones`
- `Blockers`
- `Verification Intent`
- `Exit Criteria`
- `Notes`

## Dependency Tracking

- Record upstream dependencies that must exist before the plan can finish.
- Record downstream work that depends on the plan when that relationship matters to execution order.
- Reference authoritative docs or prompts rather than relying on memory.

## Milestone Tracking

- Break work into small milestones with observable completion criteria.
- Use milestones to separate governance, scaffolding, implementation, verification, and packaging when those phases differ.
- Mark milestones complete only when the corresponding verification intent has been satisfied.

## Blocker Tracking

- Record blockers explicitly and name whether they are internal or external.
- Distinguish blocked work from intentionally deferred work.
- Remove or downgrade a blocker only when the blocking condition is actually resolved.

## Verification Intent

- State how the plan will be verified before the work is declared complete.
- Verification intent may include file checks, schema checks, tests, evals, or structural review depending on the task.
- If only structural verification is possible, say so up front.

## Entry Template

```md
### Plan ID: PX

- Title:
- Status:
- Objective:
- Scope:
- Allowed Paths:
- Dependencies:
- Milestones:
- Blockers:
- Verification Intent:
- Exit Criteria:
- Notes:
```

## Current Plan Index

### Plan ID: P00

- Title: AIDE repository constitution and operating law
- Status: Completed
- Objective: establish the root operating law, governance policies, and root planning and documentation templates
- Scope: `README.md`, root control-plane files, and `governance/` policy documents only
- Allowed Paths: `README.md`, `AGENTS.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `governance/vision.md`, `governance/support-policy.md`, `governance/naming-policy.md`, `governance/capability-levels.md`, `governance/release-policy.md`
- Dependencies: existing bootstrap control-plane commit `f2b4e72`
- Milestones: inspect current root docs; draft consistent governance set; verify conceptual anchors and required files; checkpoint a commit
- Blockers: none
- Verification Intent: file existence checks plus `rg` checks for required policy anchors and terminology
- Exit Criteria: all required files exist, the policy set is internally consistent, and verification passes
- Notes: governance only; no product implementation, inventory system, adapter code, packaging, CI, or environments in this prompt; conceptual-anchor verification passed

### Plan ID: P06

- Title: Shared-core architecture and host-adapter contract system
- Status: Completed
- Objective: define the canonical shared-core architecture, host-adapter contract, execution-mode model, and conservative shared schemas for later implementation prompts
- Scope: `specs/**`, `shared/**`, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `specs/**`, `shared/**`
- Dependencies: P00 governance law, P01 inventory and matrices, P03 through P05 host-atlas research, and the existing host-lane scaffold under `hosts/**`
- Milestones: architecture narratives created under `specs/architecture/`; shared subtree scaffold created under `shared/`; machine-readable shared schemas created under `shared/schemas/`; root planning and documentation indexes updated to record the milestone
- Blockers: none
- Verification Intent: structural verification only, using file and directory existence checks, `rg` anchor checks for core contract terms and execution modes, and an allowed-path audit over the git diff
- Exit Criteria: architecture docs exist and are internally consistent, shared subtree directories and schema placeholders exist, planning or documentation indexes are updated, and verification passes
- Notes: architectural only; executable shared-core logic, host-adapter implementation, packaging, CI, environments, and eval wiring remain deferred

### Plan ID: P07

- Title: Environment, lab, and acquisition framework
- Status: Completed
- Objective: define the environment and lab control plane for acquisition, media provenance, bring-up status, snapshots, blockers, and archival tracking
- Scope: `environments/**`, `labs/**`, `inventory/legal-acquisition.yaml`, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `inventory/legal-acquisition.yaml`, `environments/**`, `labs/**`
- Dependencies: P00 governance law, P01 inventory and matrices, P06 architecture contracts, and the existing placeholder `environments/` and `labs/` directories
- Milestones: environment model and acquisition policy docs created; environment subtree scaffold and machine-readable catalogs created; lab workflow and registers created; root planning and documentation indexes updated to record the phase
- Blockers: none
- Verification Intent: structural verification only, using file and directory existence checks, `rg` anchor checks for environment and acquisition vocabulary, and an allowed-path audit over the git diff
- Exit Criteria: environment and lab frameworks exist and are internally consistent, acquisition/legal posture is machine-readable, catalogs and registers are structurally coherent, and verification passes
- Notes: framework only; no actual media acquisition, environment bring-up, snapshots, proprietary assets, or runnable environment claims are introduced in this prompt

### Plan ID: P08

- Title: Evaluation, verification, packaging, and release framework
- Status: Completed
- Objective: define the control plane for evaluation models, verification routines, graders, packaging posture, artifact classes, release channels, and release-shape tracking
- Scope: `evals/**`, `packaging/**`, `matrices/test-matrix.yaml`, `matrices/packaging-matrix.yaml`, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `evals/**`, `packaging/**`, `matrices/test-matrix.yaml`, `matrices/packaging-matrix.yaml`
- Dependencies: P00 governance law, P01 inventory and seed matrices, P06 shared-core architecture, P07 environment and lab framework, and existing host-lane and research records
- Milestones: evaluation model and strategy docs created; eval subtree scaffold and catalogs created; packaging model and policy docs created; packaging subtree scaffold and catalogs created; test and packaging matrices refined from placeholders into planning frameworks; root planning and documentation indexes updated to record the phase
- Blockers: none
- Verification Intent: structural verification only, using file and directory existence checks, `rg` anchor checks for evaluation and packaging vocabulary, and an allowed-path audit over the git diff
- Exit Criteria: eval and packaging frameworks exist and are internally consistent, machine-readable catalogs and registers are structurally coherent, matrices are meaningfully refined, and verification passes
- Notes: framework only; no executable tests, graders, packaging automation, manifests with real shipping content, release binaries, or CI workflows are introduced in this prompt

### Plan ID: P09

- Title: Cross-host boot-slice specification and oldest-first rollout plan
- Status: Completed
- Objective: define the first implementation slice, lane-by-lane acceptance criteria, degraded or blocked handling, and an oldest-first rollout structure aligned to the research corpus
- Scope: `specs/boot-slice/**`, `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `specs/boot-slice/**`, `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`
- Dependencies: P00 through P08, especially host-atlas research, capability matrices, shared-core contract architecture, and evaluation framework documents
- Milestones: boot-slice specification set created; machine-readable boot-slice and rollout manifests created; feature and test matrices refined for the first slice; eval catalog and verification definitions refined for boot-slice planning; root planning and documentation indexes updated
- Blockers: none
- Verification Intent: structural verification only, using file and directory existence checks, `rg` anchor checks for boot-slice and rollout vocabulary, lane-id checks against the rollout manifest, and an allowed-path audit over the git diff
- Exit Criteria: the boot-slice specification exists and is internally consistent, the rollout plan covers all committed lanes, degraded or blocked handling is explicit, matrices and eval catalogs are meaningfully refined, and verification passes
- Notes: specification only; no shared-core logic, host-adapter implementation, CI, or runtime eval results are introduced in this prompt

### Plan ID: P10

- Title: Shared-core boot-slice implementation
- Status: Completed
- Objective: implement the shared-core portion of the first boot slice, including deterministic request and response handling, capability reporting, unavailable or deferred reporting, and a host-agnostic CLI bridge
- Scope: `shared/**`, `fixtures/**`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, `evals/runs/**`, `evals/reports/**`, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `shared/**`, `fixtures/**`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, `evals/runs/**`, `evals/reports/**`
- Dependencies: P06 shared-core architecture, P08 evaluation framework, P09 boot-slice specification, and the existing shared schema set under `shared/schemas/**`
- Milestones: implement the minimal shared-core runtime and CLI bridge; add deterministic boot-slice request or response fixtures; add standard-library tests for dispatch and CLI smoke; record eval definitions and a run record for the shared-core slice; update root planning and documentation indexes
- Blockers: none
- Verification Intent: executable verification, using file existence checks, `py -3 -m unittest discover -s shared/tests -t .`, direct `py -3 -m shared.cli` smoke invocation against fixtures, anchor checks for core contract vocabulary, and an allowed-path audit over repository changes
- Exit Criteria: the shared-core boot slice is implemented, tests pass, the CLI smoke case passes, capability and unavailable or deferred reporting are present, fixtures and eval records exist, and verification passes
- Notes: bootstrap runtime choice is pure Python 3 with the standard library only; host adapters, local-service daemons, packaging flows, and later capabilities remain deferred
