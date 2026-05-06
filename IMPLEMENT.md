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
