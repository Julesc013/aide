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
