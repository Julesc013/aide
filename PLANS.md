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

### Plan ID: P11

- Title: Microsoft host boot-slice implementations
- Status: Completed
- Objective: implement the Microsoft host-family side of the first boot slice using thin lane-local artifacts that reuse the shared-core CLI bridge where honest and explicit blocked records where native proof is not yet reproducible
- Scope: `hosts/microsoft/**`, Microsoft-related matrix rows, Microsoft eval records and run logs, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `hosts/microsoft/**`, `matrices/support-matrix.yaml`, `matrices/capability-matrix.yaml`, `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, `evals/runs/**`, `evals/reports/**`
- Dependencies: P03 Microsoft ecosystem atlas, P09 boot-slice lane acceptance rules, P10 shared-core CLI bridge and deterministic runtime fixtures, and the existing Microsoft lane scaffold under `hosts/microsoft/**`
- Milestones: implement runnable degraded cli-bridge proofs for feasible Microsoft lanes; add explicit blocked-proof artifacts for native archival or embedded lanes that cannot be verified honestly here; refine Microsoft support, capability, feature, and test matrices to match actual proof posture; record Microsoft eval status and a phase run log; update root planning and documentation indexes
- Blockers: no reproducible VSSDK-capable Visual Studio environment for `vsix-v2-vssdk`; no reproducible Visual Studio for Mac archival environment for `monodevelop-addin`
- Verification Intent: executable verification where possible, using shared-core unit tests, direct lane-local cli-bridge smoke invocations for runnable Microsoft lanes, structural blocked-proof checks for non-runnable lanes, anchor checks for Microsoft boot-slice vocabulary, and an allowed-path audit over repository changes
- Exit Criteria: every Microsoft lane has a runnable, degraded, or explicitly blocked boot-slice proof; shared-core behavior is reused rather than duplicated; Microsoft matrices and eval records match actual outcomes; and verification passes
- Notes: P11 stays Microsoft-only and does not claim Apple or CodeWarrior host success; `local-service` remains deferred even for the modern extensibility lane

### Plan ID: P12

- Title: Apple host boot-slice implementations
- Status: Completed
- Objective: implement the Apple host-family side of the first boot slice using a runnable thin companion proof and an explicit blocked structural XcodeKit proof that keeps the native editor target visible without inventing macOS or Xcode runtime success
- Scope: `hosts/apple/**`, Apple-related matrix rows, Apple eval records and run logs, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `hosts/apple/**`, `matrices/support-matrix.yaml`, `matrices/capability-matrix.yaml`, `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, `evals/runs/**`, `evals/reports/**`
- Dependencies: P04 Apple ecosystem atlas, P09 boot-slice lane acceptance rules, P10 shared-core CLI bridge and deterministic runtime fixtures, and the existing Apple lane scaffold under `hosts/apple/**`
- Milestones: implement a runnable `cli-bridge` companion proof; add explicit blocked structural records for the required native `xcodekit` lane; refine Apple support, capability, feature, and test matrices to match actual proof posture; record Apple eval status and a phase run log; update root planning and documentation indexes
- Blockers: no reproducible macOS or Xcode environment for `xcodekit`; no verified containing-app or extension packaging flow for the `xcodekit` lane; no verified embedded Swift or XcodeKit bridge to the shared-core runtime under current prompt scope
- Verification Intent: executable verification where possible, using shared-core unit tests, direct lane-local cli-bridge smoke invocation for the Apple companion lane, structural blocked-proof checks for the non-runnable XcodeKit lane, anchor checks for Apple boot-slice vocabulary, and an allowed-path audit over repository changes
- Exit Criteria: every Apple lane has a runnable, degraded, or explicitly blocked boot-slice proof; shared-core behavior is reused rather than duplicated; Apple matrices and eval records match actual outcomes; and verification passes
- Notes: P12 stays Apple-only and does not claim Microsoft or CodeWarrior host success; `xcodekit` remains a required native editor target even when its current proof is structural and blocked

### Plan ID: P13

- Title: Legacy host boot-slice implementations and backlog stabilization
- Status: Completed
- Objective: implement the committed CodeWarrior boot-slice wave, keep both legacy lanes honest about runnable versus archival-native limits, and stabilize the broader legacy candidate backlog using what this implementation wave revealed
- Scope: `hosts/metrowerks/**`, `inventory/legacy-ide-families.yaml`, legacy-related matrix rows, legacy eval records and run logs, and root planning or documentation indexes only
- Allowed Paths: `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `hosts/metrowerks/**`, `inventory/legacy-ide-families.yaml`, `matrices/support-matrix.yaml`, `matrices/capability-matrix.yaml`, `matrices/feature-coverage.yaml`, `matrices/test-matrix.yaml`, `evals/catalogs/eval-catalog.yaml`, `evals/catalogs/verification-catalog.yaml`, `evals/runs/**`, `evals/reports/**`
- Dependencies: P05 CodeWarrior and legacy atlas research, P09 boot-slice lane acceptance rules, P10 shared-core CLI bridge and deterministic fixtures, and the existing CodeWarrior lane scaffold under `hosts/metrowerks/**`
- Milestones: implement runnable cli-bridge proofs for the committed `ide-sdk` and `companion` lanes; add native-adjacent structural metadata for the archival-native lane; refine legacy support, capability, feature, and test matrices to match actual proof posture; stabilize `inventory/legacy-ide-families.yaml` using post-CodeWarrior guidance; record legacy eval status and a CodeWarrior run log; update root planning and documentation indexes
- Blockers: no reproducible historical CodeWarrior environment for honest in-host IDE SDK or COM loading; no active-document capture path for optional `ide-sdk` editor-marker proof; later Eclipse-era CodeWarrior contract boundaries remain unresolved under the current native lane umbrella
- Verification Intent: executable verification where possible, using shared-core unit tests, direct lane-local cli-bridge smoke invocations for runnable CodeWarrior lanes, structural verification of native-adjacent metadata for `ide-sdk`, anchor checks for legacy boot-slice and backlog vocabulary, and an allowed-path audit over repository changes
- Exit Criteria: every committed legacy lane has a runnable, degraded, or explicitly blocked boot-slice proof; shared-core behavior is reused rather than duplicated; legacy matrices and eval records match actual outcomes; the broader legacy backlog is conservatively stabilized; and verification passes
- Notes: P13 stays CodeWarrior-only for implementation work and does not promote any backlog candidate into a new committed `hosts/` lane

### Plan ID: P14

- Title: Documentation normalization, roadmap, contributor guidance, and maintenance automation baseline
- Status: Completed
- Objective: consolidate the repository after the first implementation wave by normalizing root docs, creating contributor and roadmap guidance, establishing the maintenance baseline, adding repo-local maintenance skills, and recording a post-P13 audit
- Scope: root documentation, `scripts/**`, `.agents/**`, `evals/reports/**`, and root planning or documentation indexes only
- Allowed Paths: `README.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `MAINTENANCE.md`, `CHANGELOG.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `scripts/**`, `.agents/README.md`, `.agents/skills/**`, `evals/reports/**`
- Dependencies: P00 through P13, especially the root control-plane files, current matrix posture, existing repo-local skills, and the first host-family proof waves
- Milestones: normalize `README.md`; add contributor, roadmap, maintenance, and changelog docs; create maintenance task catalog and reusable checklists; add maintenance-oriented repo-local skills; record the bootstrap-phase audit and blocker summary; update root planning and documentation indexes
- Blockers: none for the consolidation phase itself; the new docs must preserve existing blocked and deferred technical areas rather than trying to resolve them
- Verification Intent: structural verification using file and directory existence checks, skill frontmatter checks, anchor scans for roadmap and maintenance vocabulary, and an allowed-path audit over repository changes
- Exit Criteria: the repo has coherent contributor, roadmap, changelog, and maintenance docs; maintenance assets and repo-local skills exist; the bootstrap-phase audit exists; root indexes are updated; and verification passes
- Notes: P14 is consolidation-only and does not add new product features, broaden the boot slice, or create new host families

### Plan ID: P15

- Title: AIDE self-bootstrap queue scaffold
- Status: Completed
- Objective: create the minimal filesystem queue, policies, repo instructions, scripts, and first Q00 ExecPlan needed for future self-hosting work to proceed from repository state rather than chat state
- Scope: `.aide/**`, `.agents/**`, `scripts/**`, `docs/**`, `AGENTS.md`, `README.md`, `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md`
- Allowed Paths: `AGENTS.md`, `README.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `docs/**`, `.aide/**`, `.agents/**`, `scripts/**`
- Dependencies: P00 through P14, especially current operating law, root documentation indexes, repo-local skills, and maintenance automation boundaries
- Milestones: create `.aide/profile.yaml` and `.aide/toolchain.lock`; create queue policy, index, and Q00 task packet; add autonomy, bypass, and review-gate policies; add queue, ExecPlan, and review skills; add conservative queue scripts; document self-bootstrap usage; update root indexes
- Blockers: none for the scaffold itself; future queue items remain pending until Q00 is processed and reviewed
- Verification Intent: structural file-existence checks, Python syntax checks for queue scripts, read-only queue script execution, anchor scans for canonical queue policy, and an allowed-path audit over repository changes
- Exit Criteria: all required scaffold files exist, queue scripts run without external dependencies, Q00 remains ready for a future worker, root docs link the queue, evidence records validation, and the change is committed
- Notes: P15 is a self-bootstrap scaffold only; it does not implement Runtime, Hosts, Commander, Mobile, app surfaces, provider integrations, or Q01 through Q04

## Reboot Queue Plan Index

### Queue ID: Q00-bootstrap-audit

- Title: Baseline freeze and reboot audit
- Status: Needs Review
- Objective: produce a factual, evidence-backed baseline freeze for the in-place AIDE reboot while preserving P00 through P15 history
- Scope: reboot baseline docs, root documentation links, Q00 status and evidence, and queue plan visibility through Q08
- Allowed Paths: `README.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, `docs/**`, `.aide/**`, `.agents/**`, `scripts/**`, `AGENTS.md`
- Dependencies: P00 through P15 and the Q00 queue task packet
- Milestones: create bootstrap-era constitution; create reboot charter; create repo census; create reboot roadmap; update root indexes; write Q00 evidence; run validation; stop at review
- Blockers: none identified at planning time
- Verification Intent: required file checks, queue helper execution, anchor scans for the reboot model, changed-path audit, and documentation sanity checks
- Exit Criteria: Q00 documents and evidence exist, root docs link them, Q01 through Q08 are visible as queue plan, validation is recorded, and status moves to `needs_review`
- Notes: Q00 does not implement Q01 or later work, move files, build runtime or host surfaces, or change forbidden paths

### Queue ID: Q01-documentation-split

- Title: Documentation split and canonical architecture
- Status: Needs Review
- Objective: split reboot documentation into durable families and document the canonical model around AIDE Core, AIDE Hosts, AIDE Bridges, the internal Core split, and the first shipped stack
- Scope: documentation family indexes, focused charters, ADR-like decisions, roadmap/reference records, root documentation pointers, Q01 queue status, and Q01 evidence
- Allowed Paths: `docs/**`, `README.md`, `DOCUMENTATION.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`, `.aide/queue/Q01-documentation-split/**`, `.aide/queue/index.yaml`
- Dependencies: Q00 baseline records and explicit Q01 implementation authorization while Q00 remains `needs_review`
- Milestones: create documentation family indexes; add Core, Contract, Harness, Compatibility, Hosts, Bridges, Control, and SDK charters; add initial reboot decisions; add migration and terminology references; update root docs; write evidence; run validation; stop at review
- Blockers: none identified during implementation; Q00 still needs review before the reboot baseline is accepted
- Verification Intent: structural file checks, queue helper execution, terminology scans, documentation sanity checks, and an allowed-path audit over the diff
- Exit Criteria: Q01 documentation families are navigable, root docs point to them, evidence and validation are recorded, no forbidden paths are modified, and status moves to `needs_review`
- Notes: Q01 is documentation-only and does not implement Q02, Runtime, Hosts, Commander, Mobile, IDE extensions, provider adapters, app surfaces, or automation

### Queue ID: Q02-structural-skeleton

- Title: Minimal self-hosting structural skeleton
- Status: Needs Review
- Objective: introduce target `core/`, new host-category, and `bridges/` README-only skeletons without moving bootstrap-era implementation
- Scope: target skeleton directories, README ownership boundaries, structural migration map, root documentation pointers, Q02 queue status, and Q02 evidence
- Allowed Paths: `core/**`, `hosts/README.md`, `hosts/cli/**`, `hosts/service/**`, `hosts/commander/**`, `hosts/extensions/**`, `bridges/**`, `docs/**`, root docs, `.aide/queue/Q02-structural-skeleton/**`, and `.aide/queue/index.yaml`
- Dependencies: Q00 and Q01 outputs; both are currently `needs_review`, and Q02 proceeded only because the current human prompt explicitly authorized implementation
- Milestones: create Core skeleton; create host-category skeletons; create Dominium Bridge skeleton; add structural migration map; update root docs; write evidence; run validation; stop at review
- Blockers: none identified during implementation; Q00 and Q01 still need review before their outputs are accepted
- Verification Intent: skeleton file checks, migration-map checks, root doc checks, queue helper execution, terminology scans, lightweight shared test/import-preservation check, `git diff --check`, and allowed-path audit
- Exit Criteria: target skeleton READMEs exist, current code and proofs remain unmoved, structural map and evidence are recorded, no forbidden paths are modified, and status moves to `needs_review`
- Notes: Q02 is structure/documentation-only and does not implement Q03, Runtime, Host behavior, Commander, Mobile, IDE extensions, provider adapters, app surfaces, or autonomous service logic

### Queue ID: Q03-profile-contract-v0

- Title: Profile contract v0
- Status: Needs Review
- Objective: implement the minimal declarative `.aide/` Profile/Contract v0 for the AIDE self-hosting repo
- Scope: `.aide/` contract records, documented Contract shapes, source-of-truth references, root doc pointers, Q03 status, and Q03 evidence
- Allowed Paths: `.aide/profile.yaml`, `.aide/toolchain.lock`, `.aide/components/**`, `.aide/commands/**`, `.aide/policies/**`, `.aide/tasks/**`, `.aide/evals/**`, `.aide/adapters/**`, `.aide/compat/**`, `core/contract/**`, `docs/reference/profile-contract-v0.md`, `docs/reference/source-of-truth.md`, `AGENTS.md`, `.agents/skills/**`, root docs, `.aide/queue/Q03-profile-contract-v0/**`, and `.aide/queue/index.yaml`
- Dependencies: Q00, Q01, and Q02 outputs; all three remain `needs_review`, and Q03 proceeded only because the current human prompt explicitly authorized implementation
- Milestones: define Profile versus Harness boundaries; refine `.aide/profile.yaml` and `.aide/toolchain.lock`; add component, command, policy, task, eval, adapter, and compat declarations; document v0 shapes; add source-of-truth references; update root docs; write evidence; run validation; stop at review
- Blockers: none identified during implementation; prior queue items still need review before their outputs are accepted
- Verification Intent: required file checks, required component checks, command and policy checks, queue helper execution, terminology scans, lightweight YAML/Markdown sanity checks, `git diff --check`, and allowed-path audit
- Exit Criteria: Profile/Contract v0 records and references exist, Profile vs Harness is clear, generated artifacts remain deferred, evidence is recorded, no forbidden paths are modified, and status moves to `needs_review`
- Notes: Q03 is contract-only and does not implement Harness commands, generated downstream artifacts, Runtime, Hosts, Dominium Bridge behavior, provider adapters, app surfaces, source refactors, or Q04+ work

### Queue ID: Q04-harness-v0

- Title: Harness v0
- Status: Passed With Notes
- Objective: implement the smallest deterministic AIDE Harness v0 command surface for reading, validating, doctoring, and reporting on the Q03 Profile/Contract v0
- Scope: `scripts/aide`, `core/harness/**`, `docs/reference/harness-v0.md`, minimal root doc updates, Q04 queue status, ExecPlan updates, and evidence
- Allowed Paths: `core/harness/**`, `scripts/aide`, `docs/reference/harness-v0.md`, root docs, `.aide/queue/Q04-harness-v0/**`, and `.aide/queue/index.yaml`
- Dependencies: Q00, Q01, Q02, and Q03 outputs remain `needs_review`; this implementation proceeded under explicit human authorization and the full audit verdict `PROCEED_TO_Q04_IMPLEMENTATION`
- Milestones: implement repo-root entrypoint; add Harness modules; implement init/import/compile/validate/doctor/migrate/bakeoff; add lightweight tests; update docs and evidence; run command smoke and structural validation
- Blockers: none encountered during implementation; Q05 remains blocked until Q04 review passes
- Verification Intent: command smoke checks, `aide validate`, `aide doctor`, compile/migrate/bakeoff reports, lightweight unittest smoke, queue helper checks, generated-artifact absence checks, `git diff --check`, and allowed-path audit
- Exit Criteria: Harness v0 commands run, validation passes with warnings only, evidence is recorded, generated artifacts remain absent, and Q04 review records `PASS_WITH_NOTES`
- Notes: Q04 does not implement Q05 generated artifacts, Q06 compatibility baseline, Q07 Dominium Bridge, Runtime, Hosts, provider integrations, app surfaces, release automation, or autonomous worker execution. Q05 planning may proceed; Q05 implementation still requires its own plan and review gate.

### Queue ID: Q05-generated-artifacts-v0

- Title: Generated artifacts v0
- Status: Needs Review
- Objective: implement deterministic generated downstream artifact v0 for AIDE self-hosting guidance while keeping `.aide/` and `.aide/queue/` canonical
- Scope: bounded Harness-status refresh, generated artifact policy docs, Harness compile/validate updates, managed sections in `AGENTS.md` and selected `.agents/skills/**`, `.aide/generated/manifest.yaml`, preview-only Claude guidance, Q05 status, and Q05 evidence
- Allowed Paths: `core/harness/**`, selected `.aide/**` contract/generated paths allowed by Q05, `AGENTS.md`, `.agents/skills/**`, `docs/reference/generated-artifacts-v0.md`, source-of-truth and Harness references, root docs, `.aide/queue/Q05-generated-artifacts-v0/**`, and `.aide/queue/index.yaml`
- Dependencies: Q04 passed with notes and Q05 planning explicitly authorized the bounded Q03-era Harness wording refresh before generation
- Milestones: refresh stale Harness contract wording; document generated artifact v0; add marker and manifest helpers; add compile dry-run/preview/write behavior; add validate drift checks; generate approved managed/preview outputs; write evidence; stop at review
- Blockers: none encountered during implementation
- Verification Intent: pre/post Harness validation and doctor checks, compile dry-run/preview/write flows, command smoke checks, Harness unittest and py_compile checks, queue helper checks, marker/manifest scans, final Claude target absence checks, `git diff --check`, and allowed-path audit
- Exit Criteria: generated artifact policy, manifest, managed sections, preview output, Harness drift checks, evidence, and review-gated `needs_review` status are present without Q06+ or forbidden scope
- Notes: Q05 does not make generated artifacts canonical, create final root `CLAUDE.md`, create final `.claude/**`, implement Compatibility baseline, Dominium Bridge, Runtime, Hosts, provider adapters, app surfaces, release automation, or autonomous service logic.

### Queue ID: Q06-compatibility-baseline

- Title: Compatibility baseline
- Status: Needs Review
- Objective: implement the smallest enforceable Compatibility baseline for known AIDE repo evolution surfaces without building a full migration platform
- Scope: `.aide/compat/**`, `core/compat/**`, Harness validate/migrate compatibility checks, compatibility reference docs, minimal root docs, Q06 status, and Q06 evidence
- Allowed Paths: `core/compat/**`, targeted `core/harness/**` validate/migrate changes, `.aide/compat/**`, `.aide/toolchain.lock`, `.aide/commands/**`, `.aide/evals/**`, `.aide/generated/**` manifest refresh only, reference docs, root docs, `.aide/queue/Q06-compatibility-baseline/**`, and `.aide/queue/index.yaml`
- Dependencies: Q04 passed with notes; Q05 review evidence records `PASS_WITH_NOTES` and allows Q06 despite raw Q05 queue status remaining `needs_review`
- Milestones: define compatibility docs and records; add version, migration, and replay helpers; extend validate/migrate checks; add compatibility tests; refresh generated manifest if source inputs change; write evidence; stop at review
- Blockers: none encountered during implementation
- Verification Intent: pre/post Harness validation, doctor, migrate, compile/bakeoff checks, Harness and Compatibility unittests, py_compile, queue helper checks, compatibility record checks, `git diff --check`, and allowed-path audit
- Exit Criteria: compatibility docs and records exist, `aide validate` and `aide migrate` report Q06 baseline posture, replay baseline and upgrade/deprecation records exist, evidence is recorded, and status moves to `needs_review`
- Notes: Q06 does not implement real migrations, Dominium Bridge, Runtime, Hosts, providers, generated artifact behavior changes, release automation, or Q07+ work.

### Queue ID: Q07-dominium-bridge-baseline

- Title: Dominium Bridge baseline
- Status: Passed With Notes
- Objective: implement the smallest enforceable AIDE-side Dominium Bridge baseline so Dominium can later consume AIDE as a pinned portable repo layer under XStack strict governance
- Scope: bridge metadata, Dominium/XStack profile overlay, strict policy overlays, generated target expectations, compatibility/pinning records, bridge reference docs, minimal Harness bridge status checks, Q07 status, and Q07 evidence
- Allowed Paths: `bridges/dominium/**`, minimal `core/harness/**` bridge checks if needed, selected `.aide/**` metadata paths allowed by Q07, bridge/source-of-truth/reference docs, root docs, `.aide/queue/Q07-dominium-bridge-baseline/**`, and `.aide/queue/index.yaml`
- Dependencies: Q04 passed with notes; Q05 and Q06 review evidence record `PASS_WITH_NOTES` and allow Q07 despite raw Q05/Q06 queue status remaining `needs_review`
- Milestones: define bridge reference; define bridge metadata; define XStack boundary; define profile overlay; define strict policy overlays; define generated target expectations; define compatibility pinning; add minimal Harness bridge checks; write evidence; stop at review
- Blockers: none encountered during implementation
- Verification Intent: Harness validate, doctor, compile, and migrate checks; queue helper checks; bridge file and anchor checks; generated manifest drift awareness; `git diff --check`; allowed-path audit
- Exit Criteria: Q07 bridge docs and records exist, Harness reports structural bridge posture, generated target expectations remain metadata-only, no Dominium repo or real Dominium output is touched, evidence is recorded, and Q07 review records `PASS_WITH_NOTES`
- Notes: Q07 does not modify any Dominium repo, emit real Dominium outputs, implement Runtime, Hosts, providers, app surfaces, release automation, or Q08+ work. Q08 planning may proceed; Q08 implementation still requires its own plan, evidence, and review gate.

### Queue ID: Q08-self-hosting-automation

- Title: Self-hosting automation
- Status: Passed With Notes
- Objective: implement the smallest safe self-hosting automation scaffold so AIDE can inspect queue health, drift, doctor guidance, compatibility posture, bridge status, and follow-up recommendations without uncontrolled autonomy
- Scope: self-hosting reference docs, a report-first `aide self-check` command, bounded doctor next-step cleanup, conservative queue-runner helper improvements, non-canonical self-check report outputs, Q08 status, and Q08 evidence
- Allowed Paths: `scripts/aide`, `scripts/aide-queue-run`, read-only queue helpers only if needed, `core/harness/**`, selected `.aide/**` self-hosting declaration/report paths allowed by Q08, reference docs, root docs, `.aide/queue/Q08-self-hosting-automation/**`, and `.aide/queue/index.yaml`
- Dependencies: Q04 passed with notes; Q05 and Q06 review evidence record `PASS_WITH_NOTES` despite raw `needs_review` statuses; Q07 passed with notes and explicitly permits Q08 planning
- Milestones: define automation policy; add self-hosting reference; implement report-first self-check; keep report outputs non-canonical; improve queue runner without automatic agent invocation; fix stale doctor next-step wording; write evidence; stop at review
- Blockers: none for planning; implementation must not treat stale generated manifest or stale doctor wording as silent execution signals
- Verification Intent: pre/post Harness validate, doctor, compile dry-run, migrate, and bakeoff checks; self-check smoke; queue helper checks; Harness tests and py_compile as needed; generated manifest drift reporting; `git diff --check`; allowed-path audit
- Exit Criteria: Q08 implementation reaches `needs_review` only after self-hosting automation remains local, deterministic, report-first, non-autonomous, and evidence-backed
- Notes: Q08 implements report-first self-check and queue-runner visibility only. It does not invoke Codex or external agents automatically, call models/providers/network, auto-merge, silently refresh generated artifacts, implement Runtime/Service/Commander, or create post-Q08 work. Independent review accepted Q08 with notes; post-Q08 foundation review may proceed while generated manifest drift, command catalog metadata for `aide self-check`, and raw status nuance remain visible cleanup items.

### Queue ID: Q09-token-survival-core

- Title: State reconciliation and token survival core
- Status: Needs Review
- Objective: reconcile live post-Q08 state and add repo-only token-survival scaffolding so future work uses compact task packets, approximate token estimates, and evidence review instead of long chat history
- Scope: Q09 queue packet, post-Q08 profile/catalog/docs metadata, token budget policy, compact memory files, prompt templates, context ignore policy, AIDE Lite token-survival commands, tests, generated compact packet outputs, and evidence
- Allowed Paths: `.aide/queue/Q09-token-survival-core/**`, `.aide/queue/index.yaml`, `.aide/profile.yaml`, `.aide/toolchain.lock`, `.aide/commands/catalog.yaml`, `.aide/policies/**`, `.aide/prompts/**`, `.aide/context/**`, `.aide/memory/**`, `.aide/scripts/**`, `AGENTS.md`, root docs, selected `docs/reference/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q08 passed with notes; Q05/Q06 raw status nuance remains visible while review evidence permits later dependency use
- Milestones: reconcile stale state; add token policy and compact prompts; implement AIDE Lite doctor/validate/estimate/snapshot/pack/adapt/selftest; add tests; generate Q10 packet; write evidence; stop at review
- Blockers: none identified at planning time; generated manifest drift must be either preserved visibly or refreshed only through the reviewed Harness compile/write path
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke, AIDE Lite unit tests, `git diff --check`, and targeted secret scan
- Exit Criteria: Q09 status moved to `needs_review`, Q10 compact task packet exists with a token estimate, AGENTS.md carries token-survival guidance, validation is recorded, and no secrets/local state/raw prompt logs are committed
- Notes: Q09 does not implement Gateway, providers, model routing, local models, Runtime, Service, Commander, Mobile, MCP/A2A, cloud, autonomous loops, vector search, semantic cache, or host/app surfaces.

### Queue ID: Q10-aide-lite-hardening

- Title: AIDE Lite hardening
- Status: Needs Review
- Objective: harden the Q09 no-install AIDE Lite workflow so future queue phases can generate, validate, adapt, estimate, and self-test compact packets reliably
- Scope: Q10 queue packet, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, token-survival prompt/context/memory/policy records, generated context outputs, AGENTS token-survival managed section, root docs, and narrow Harness/doc touchpoints if needed
- Allowed Paths: `.aide/queue/Q10-aide-lite-hardening/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/policies/token-budget.yaml`, `.aide/prompts/**`, `.aide/context/**`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `.aide/generated/manifest.yaml` through compile/write only, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token-survival outputs exist and are review-ready; Q10 proceeds under explicit prompt authorization while Q09 awaits review
- Milestones: create Q10 queue packet; harden AIDE Lite helpers and commands; add deterministic write and drift behavior; expand tests; generate Q11 packet; write evidence; stop at review
- Blockers: none identified at planning time; Q09 missing-output blockers must stop Q10 if discovered
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke, `.aide/scripts/tests` unittest discovery, `git diff --check`, and targeted secret scan
- Exit Criteria: Q10 status moves to `needs_review`, Q11 compact task packet exists with token estimate, AIDE Lite commands and tests pass, adapt is deterministic, snapshot contains no raw contents, and evidence is complete
- Notes: Q10 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing ledger, full context compiler, full verifier, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q11 should build Context Compiler v0 from the compact packet generated by Q10.

### Planned Reboot Queue

- `Q01-documentation-split`: documentation split and canonical architecture; implemented and awaiting review
- `Q02-structural-skeleton`: structural skeleton; implemented and awaiting review
- `Q03-profile-contract-v0`: profile contract v0; implemented and awaiting review
- `Q04-harness-v0`: harness v0 passed review with notes
- `Q05-generated-artifacts-v0`: generated artifacts v0 implemented with managed sections, preview-only Claude guidance, manifest records, and drift checks; awaiting review
- `Q06-compatibility-baseline`: compatibility baseline implemented and awaiting review
- `Q07-dominium-bridge-baseline`: Dominium Bridge baseline passed review with notes
- `Q08-self-hosting-automation`: self-hosting automation passed review with notes
- `Q09-token-survival-core`: state reconciliation and token survival core awaiting review
- `Q10-aide-lite-hardening`: AIDE Lite hardening awaiting review
- `Q11-context-compiler-v0`: Context Compiler v0 awaiting review
- `Q12-verifier-v0`: Verifier v0 awaiting review
- `Q13-evidence-review-workflow`: Evidence Review Workflow awaiting review
- `Q14-token-ledger-savings-report`: Token Ledger and Savings Report awaiting review
- `Q15-golden-tasks-v0`: Golden Tasks v0 awaiting review
- `Q16-outcome-controller-v0`: Outcome Controller v0 in progress

### Queue ID: Q11-context-compiler-v0

- Title: Context Compiler v0
- Status: Needs Review
- Objective: implement deterministic repo-local context maps, test maps, context indexes, exact refs, and context packets so future queue phases can avoid whole-repo or long-history prompting
- Scope: Q11 queue packet, `.aide/context/**`, AIDE Lite index/context/map behavior, `.aide/scripts/tests/**`, selected token-survival prompt/memory/config updates, optional AIDE Lite command metadata, root docs, selected reference/roadmap docs, and narrow Harness test/doc touchpoints if needed
- Allowed Paths: `.aide/queue/Q11-context-compiler-v0/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/context/**`, `.aide/policies/token-budget.yaml`, `.aide/prompts/compact-task.md`, `.aide/prompts/codex-token-mode.md`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token-survival outputs and Q10 AIDE Lite hardening outputs exist and are review-ready; Q11 proceeds under explicit prompt authorization while Q09/Q10 await review
- Milestones: create Q11 queue packet; add context compiler config; extend AIDE Lite index/context/map behavior; generate repo-map/test-map/context-index/context packet/Q12 packet; add tests; update docs and evidence; stop at review
- Blockers: none identified at planning time; profile current-focus staleness remains visible because Q11 does not allow profile edits
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including index/context, `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scan
- Exit Criteria: Q11 status moves to `needs_review`, context artifacts exist without raw file dumps, AIDE Lite commands/tests pass, Q12 compact task packet exists with context refs, and evidence is complete
- Notes: Q11 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing ledger, embeddings, vector search, semantic cache, full verifier, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q12 should add Verifier v0 using the context-backed compact packet generated by Q11.

### Queue ID: Q12-verifier-v0

- Title: Verifier v0
- Status: Needs Review
- Objective: implement deterministic repo-local mechanical verification so future AIDE phases can check evidence packets, task packets, file references, line refs, changed-file scope, adapter drift, context packet shape, token warnings, and obvious secret risks before premium-model review
- Scope: Q12 queue packet, `.aide/verification/**`, `.aide/policies/verification.yaml`, AIDE Lite verify behavior, `.aide/scripts/tests/**`, selected prompt/context/memory/catalog updates, root docs, selected reference/roadmap docs, generated verification report, and Q12 evidence
- Allowed Paths: `.aide/queue/Q12-verifier-v0/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/verification/**`, `.aide/policies/verification.yaml`, `.aide/policies/token-budget.yaml`, `.aide/context/**`, `.aide/prompts/evidence-review.md`, `.aide/prompts/compact-task.md`, `.aide/prompts/codex-token-mode.md`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token-survival outputs, Q10 AIDE Lite hardening outputs, and Q11 context compiler outputs exist and are review-ready; Q12 proceeds under explicit prompt authorization while Q09/Q10/Q11 await review
- Milestones: create Q12 queue packet; add verifier policies/templates; extend AIDE Lite verify behavior; add tests and fixtures; generate latest verification report and Q13 packet; update docs/evidence; stop at review
- Blockers: none identified at planning time; generated manifest drift and raw review-gate nuance remain visible existing warnings
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including verify variants, `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scan
- Exit Criteria: Q12 status moved to `needs_review`, verifier command and tests pass, latest verification report exists, Q13 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q12 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing ledger, golden tasks, LLM-as-judge, automatic repair, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q13 should build the Evidence Review Workflow from Q12 verifier output.

### Queue ID: Q13-evidence-review-workflow

- Title: Evidence Review Workflow
- Status: Needs Review
- Objective: implement deterministic repo-local review-packet generation so GPT-5.5 or a human reviewer can judge compact evidence, verifier output, validation summaries, changed-file summaries, token summaries, risks, and scope boundaries without full chat history or whole repo context
- Scope: Q13 queue packet, `.aide/verification/review-decision-policy.yaml`, review-packet template, evidence-review prompt, AIDE Lite `review-pack` behavior, review-packet validation, `.aide/scripts/tests/**`, generated latest review/task packets, selected prompt/context/memory/catalog updates, root docs, selected reference/roadmap docs, and Q13 evidence
- Allowed Paths: `.aide/queue/Q13-evidence-review-workflow/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/verification/**`, `.aide/policies/verification.yaml`, `.aide/policies/token-budget.yaml`, `.aide/context/**`, `.aide/prompts/evidence-review.md`, `.aide/prompts/compact-task.md`, `.aide/prompts/codex-token-mode.md`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token-survival outputs, Q10 AIDE Lite hardening outputs, Q11 context compiler outputs, and Q12 verifier outputs exist and are review-ready; Q13 proceeds under explicit prompt authorization while Q09-Q12 await review
- Milestones: create Q13 queue packet; refine evidence-review prompt/template/policy; extend AIDE Lite `review-pack`; add review-packet validation and tests; generate latest review packet and Q14 task packet; update docs/evidence; stop at review
- Blockers: none identified at planning time; generated manifest drift and raw review-gate nuance remain visible existing warnings
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including review-pack and verify --review-packet, `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scan
- Exit Criteria: Q13 status moved to `needs_review`, review-pack command and tests pass, latest review packet exists, Q14 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q13 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing ledger, golden tasks, LLM-as-judge automation, automatic GPT calls, automatic repair, full semantic diff analysis, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q14 should formalize token ledger and savings reporting from Q13 packets.

### Queue ID: Q14-token-ledger-savings-report

- Title: Token Ledger and Savings Report
- Status: Needs Review
- Objective: implement deterministic repo-local estimated token accounting so future AIDE phases can record packet/report sizes, compare compact surfaces to named naive baselines, warn on budgets or regressions, and avoid raw prompt/response storage
- Scope: Q14 queue packet, `.aide/policies/token-ledger.yaml`, `.aide/reports/**`, AIDE Lite `ledger` behavior, budget/regression helpers, `.aide/scripts/tests/**`, generated latest task/review/report artifacts, selected prompt/context/memory/catalog updates, root docs, selected reference/roadmap docs, and Q14 evidence
- Allowed Paths: `.aide/queue/Q14-token-ledger-savings-report/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/policies/token-budget.yaml`, `.aide/policies/token-ledger.yaml`, `.aide/reports/**`, `.aide/context/**`, `.aide/prompts/compact-task.md`, `.aide/prompts/evidence-review.md`, `.aide/prompts/codex-token-mode.md`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token-survival outputs, Q10 AIDE Lite hardening outputs, Q11 context compiler outputs, Q12 verifier outputs, and Q13 review-packet outputs exist and are review-ready; Q14 proceeds under explicit prompt authorization while Q09-Q13 await review
- Milestones: create Q14 queue packet; add token-ledger policy and baseline reports; extend AIDE Lite with ledger scan/add/report/compare; add budget/regression tests; generate ledger records, savings summary, Q15 task packet, and review artifacts; update docs/evidence; stop at review
- Blockers: none identified at planning time; generated manifest drift and raw review-gate nuance remain visible existing warnings
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including ledger scan/report/compare, `.aide/scripts/tests` discovery, `git diff --check`, and targeted secret scan
- Exit Criteria: Q14 status moved to `needs_review`, ledger commands and tests pass, token ledger JSONL and savings summary exist, Q15 compact task packet exists, baseline comparison is recorded, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q14 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing integration, real API usage accounting, golden tasks, LLM-as-judge, automatic GPT review, automatic repair, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q15 should add deterministic Golden Tasks v0 quality scaffolding.

### Queue ID: Q15-golden-tasks-v0

- Title: Golden Tasks v0
- Status: Needs Review
- Objective: implement deterministic repo-local golden task quality gates so token-saving workflow changes can prove compact task packets, context packets, verifier failure detection, review packets, token ledger metadata, and adapter managed-section determinism still preserve required behavior
- Scope: Q15 queue packet, `.aide/policies/evals.yaml`, `.aide/evals/**`, AIDE Lite `eval list/run/report` behavior, `.aide/scripts/tests/**`, generated eval/context/review/token report artifacts, selected prompt/context/memory/catalog updates, root docs, selected reference/roadmap docs, and Q15 evidence
- Allowed Paths: `.aide/queue/Q15-golden-tasks-v0/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/evals/**`, `.aide/policies/evals.yaml`, selected token/verifier policies, `.aide/reports/**`, `.aide/context/**`, `.aide/prompts/**`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token survival, Q10 AIDE Lite hardening, Q11 context compiler, Q12 verifier, Q13 evidence review, and Q14 token ledger outputs exist and are review-ready; Q15 proceeds under explicit prompt authorization while Q09-Q14 await review
- Milestones: create Q15 queue packet; add eval policy and golden task catalog; extend AIDE Lite with eval list/run/report; add golden task tests; generate latest golden-task reports and Q16 compact task packet; update docs/evidence; stop at review
- Blockers: none identified at planning time; generated manifest drift and raw review-gate nuance remain visible existing warnings
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including eval list/run/report, direct `.aide/scripts/tests` discovery, documented hidden-path discovery check, `git diff --check`, and targeted secret scan
- Exit Criteria: Q15 status moved to `needs_review`, eval commands and tests pass, latest golden-task JSON/Markdown reports exist, Q16 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q15 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing integration, external coding benchmarks, LLM-as-judge, automatic GPT review, automatic repair, Q16 Outcome Controller recommendations, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q16 should consume Q15 token-quality signals.

### Queue ID: Q16-outcome-controller-v0

- Title: Outcome Controller v0
- Status: Running
- Objective: implement deterministic repo-local advisory outcome analysis so token, verifier, review, context, validation, and golden-task signals produce bounded recommendations without unsafe autonomy
- Scope: Q16 queue packet, `.aide/policies/controller.yaml`, `.aide/controller/**`, AIDE Lite outcome/optimize behavior, `.aide/scripts/tests/**`, generated controller/context/review/token report artifacts, selected prompt/memory/catalog updates, root docs, selected reference/roadmap docs, and Q16 evidence
- Allowed Paths: `.aide/queue/Q16-outcome-controller-v0/**`, `.aide/queue/index.yaml`, `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, `.aide/controller/**`, `.aide/policies/controller.yaml`, selected token/verifier/eval policies, `.aide/reports/**`, `.aide/evals/runs/**`, `.aide/context/**`, `.aide/prompts/**`, `.aide/memory/**`, `.aide/commands/catalog.yaml`, `AGENTS.md`, root docs, selected `docs/reference/**`, `docs/roadmap/**`, `core/harness/**`, and `scripts/aide`
- Dependencies: Q09 token survival, Q10 AIDE Lite hardening, Q11 context compiler, Q12 verifier, Q13 evidence review, Q14 token ledger, and Q15 golden tasks outputs exist and are review-ready; Q16 proceeds under explicit prompt authorization while Q09-Q15 await review
- Milestones: create Q16 queue packet; add controller policy and records; extend AIDE Lite with outcome report/add and optimize suggest; add controller tests; generate latest controller reports and Q17 task packet; update docs/evidence; stop at review
- Blockers: none identified at planning time; baseline Q15 eval WARN and generated manifest drift remain visible signals rather than hidden state
- Verification Intent: Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE Lite command smoke including outcome/optimize, direct `.aide/scripts/tests` discovery, documented hidden-path discovery check, `git diff --check`, and targeted secret scan
- Exit Criteria: Q16 status moves to `needs_review`, outcome/optimize commands and tests pass, latest outcome/recommendation reports exist, Q17 compact task packet exists, evidence is complete, and no secrets/local state/raw prompt logs are committed
- Notes: Q16 does not implement Gateway, providers, model routing, local models, exact tokenizer, provider billing integration, automatic prompt/policy/route mutation, LLM-as-judge, automatic GPT review, automatic repair, Q17 Router Profile behavior, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app surfaces, or autonomous loops. Q17 should define Router Profile v0 from advisory signals only.
