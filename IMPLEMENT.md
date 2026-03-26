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
