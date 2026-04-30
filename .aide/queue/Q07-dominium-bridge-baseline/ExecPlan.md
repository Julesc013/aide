# Q07 ExecPlan: Dominium Bridge Baseline

## Purpose

Q07 will implement the first AIDE-side Dominium Bridge baseline. The baseline must define how Dominium can later consume AIDE as a pinned portable repo layer under XStack strict governance without making AIDE Dominium-shaped and without implementing Dominium product/runtime semantics.

Q07 is intentionally small. It creates bridge metadata, profile overlays, policy overlays, generated-target expectations, compatibility/pinning records, validation expectations, and human reference docs. It does not modify any Dominium repository, generate real Dominium outputs, implement Runtime, implement Hosts, call providers/models, add app surfaces, or build autonomous service logic.

## Background And Current Repo Context

AIDE is being rebooted in place. Bootstrap-era governance, shared-core implementation, host proofs, inventories, matrices, research, environments, evals, packaging, and evidence remain preserved.

Current facts verified during Q07 planning:

- Q04 Harness v0 is implemented and passed review with `PASS_WITH_NOTES`.
- Q05 generated artifacts v0 is implemented and reviewed with `PASS_WITH_NOTES`.
- Q06 Compatibility baseline is implemented and reviewed with `PASS_WITH_NOTES`.
- Q05 and Q06 raw queue statuses intentionally remain `needs_review` because review-only tasks avoided updating `.aide/queue/index.yaml`, which is part of the Q05 generated manifest source fingerprint.
- Q06 review evidence explicitly says Q07 planning may proceed.
- `py -3 scripts/aide validate`, `doctor`, `compile`, and `migrate` run successfully with review-gate warnings only.
- `bridges/dominium/**` currently contains README-only Q02 skeletons.
- ADR-0006 states that XStack remains Dominium-local and must not be genericized into AIDE doctrine.
- `.aide/profile.yaml` and generated summaries still contain some Q05/Q06-era stale wording. Q06 review says this is cleanup before Q08 or broader automation, not a Q07 planning blocker.

The future Q07 worker must re-verify these facts before implementation.

## Scope

Q07 implementation should:

- create `docs/reference/dominium-bridge.md`;
- update bridge skeleton docs under `bridges/dominium/**`;
- add a minimal `bridges/dominium/bridge.yaml`;
- add AIDE-side Dominium adoption and validation references;
- add XStack scope and portable mapping records that keep XStack Dominium-local;
- add a Dominium/XStack AIDE profile overlay that extends, but does not replace, `.aide/profile.yaml`;
- add strict policy overlays that do not weaken baseline AIDE policy;
- add generator target metadata for future Dominium outputs without emitting those outputs;
- add compatibility/pinning records that reference Q06 Compatibility baseline;
- optionally add minimal Harness validate/doctor/compile structural checks for bridge files and bridge target plans;
- update root/reference docs minimally;
- write Q07 evidence and stop at review.

## Non-goals

- Do not implement Dominium product semantics.
- Do not modify or create files in any external Dominium repository.
- Do not implement Dominium Runtime, XStack internals, or proof execution.
- Do not make XStack generic AIDE doctrine.
- Do not implement Runtime, Service, Hosts, Commander, Mobile, IDE extensions, provider adapters, browser bridges, model calls, app surfaces, release automation, or autonomous service logic.
- Do not generate real Dominium repo outputs.
- Do not create final Claude/Codex/OpenHands Dominium target files.
- Do not alter generated artifact behavior beyond bridge target plan reporting if explicitly planned.
- Do not implement Q08 or later work.
- Do not delete or move bootstrap-era records.

## Allowed Paths For Q07 Implementation

- `bridges/dominium/**`
- `core/harness/**` only for minimal bridge-aware validate/doctor/compile status checks described by this plan
- `.aide/components/**` only if needed to update existing bridge component metadata
- `.aide/commands/**` only if needed to record bridge-aware validate/doctor/compile support
- `.aide/evals/**` only if needed for bridge validation declarations
- `.aide/compat/**` only if needed for bridge compatibility/pinning metadata
- `.aide/generated/**` only if Q07 records bridge target plans and does not emit real Dominium outputs
- `docs/reference/dominium-bridge.md`
- `docs/reference/compatibility-baseline.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/source-of-truth.md`
- `docs/charters/bridges-charter.md`
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q07-dominium-bridge-baseline/**`
- `.aide/queue/index.yaml`

## Forbidden Paths For Q07 Implementation

- Any external Dominium repository path
- `shared/**`
- existing `hosts/**` implementation/proof files
- `core/runtime/**`
- `core/control/**` except conceptual docs references if needed
- `core/sdk/**`
- `governance/**`
- `inventory/**`
- `matrices/**`
- `research/**`
- `specs/**`
- `environments/**`
- `labs/**`
- `evals/**` except specifically allowed AIDE bridge validation declarations under `.aide/evals/**`
- `packaging/**`
- provider/model integrations
- web search integrations
- local model integrations
- runtime/broker/service code
- IDE/app/host code
- release/package automation
- real Dominium generated outputs
- Q08 implementation

## Dominium Bridge Scope

The minimum bridge unit is a small AIDE-side bridge packet:

- bridge metadata;
- Dominium/XStack profile overlay;
- strict policy overlays;
- generated target expectation metadata;
- validation gate declarations;
- compatibility and pinning rules;
- adoption guide.

The bridge owns mapping and guardrails. It does not own durable AIDE semantics and does not own Dominium product semantics.

Q07 should define that Dominium Bridge owns:

- mapping AIDE Contract/Harness/Compatibility/generated-artifact concepts into Dominium/XStack expectations;
- stricter review, proof, and audit overlays for Dominium-local use;
- compatibility pinning rules for consuming AIDE;
- generated target expectations for future Dominium agent surfaces;
- validation expectations for future bridge adoption;
- adoption guidance for a later Dominium repo task.

Q07 should define that Dominium Bridge does not own:

- Dominium application behavior;
- Dominium Runtime or XStack internals;
- model/provider/tool execution;
- generic AIDE Core semantics;
- host/app/IDE extension implementation;
- real generated files inside a Dominium repository.

## XStack Boundary

XStack remains Dominium-local and strict. Q07 must describe XStack as a governance/proof profile above AIDE, not a generic AIDE product layer.

Planned XStack records:

- `bridges/dominium/xstack/scope.md` explains local-only scope and non-goals.
- `bridges/dominium/xstack/portable-mapping.yaml` maps portable AIDE concepts to Dominium/XStack expectations without claiming full XStack implementation.

XStack may require stricter gates than baseline AIDE, but it must not weaken AIDE base policies.

## Stack Ordering

The Q07 stack order is:

1. AIDE portable Core records: Contract, Harness, Compatibility, generated-artifact rules, queue policy, and evidence.
2. Dominium Bridge: AIDE-side bridge metadata, overlays, target expectations, compatibility pinning, and validation declarations.
3. XStack: Dominium-local strict governance and proof profile above AIDE.
4. Dominium repo: future consumer outside Q07 scope.

AIDE remains portable. Dominium/XStack may consume AIDE, but AIDE does not become Dominium-owned.

## Profile Overlay Model

Q07 should add `bridges/dominium/profiles/dominium-xstack.profile.yaml`.

The profile overlay should:

- identify itself as an overlay, not canonical AIDE Profile replacement;
- reference `.aide/profile.yaml` and `aide.profile-contract.v0`;
- declare stricter Dominium/XStack posture such as stricter review gates, proof evidence, compatibility pinning, and generated target review;
- mark Dominium-only fields as Dominium-local;
- mark Runtime, provider, host, app, and external repo semantics as out of scope.

## Policy Overlay Model

Q07 should add strict policy overlays under `bridges/dominium/policies/**`.

Suggested files:

- `review-gates.yaml`
- `proof-gates.yaml`
- `generated-artifacts.yaml`
- `README.md`

Policy overlays must:

- state `base_policy_relation: stricter-than-aide`;
- not weaken `.aide/policies/**` or `.aide/queue/policy.yaml`;
- require evidence before Dominium adoption;
- require reviewed pin changes;
- require generated target review before real Dominium outputs are written;
- prohibit autonomous bypass of AIDE queue/review policy.

## Generated-Target Expectation Model

Q07 should add generator metadata under `bridges/dominium/generators/**`, not actual generated Dominium outputs.

Suggested file: `bridges/dominium/generators/targets.yaml`.

Target classes should include:

- `AGENTS.md` or managed sections in the Dominium repo;
- `.agents/skills/*` for Dominium-local agent guidance;
- Claude/Codex/OpenHands target files only as future target classes;
- bridge manifest or adoption report outputs only as planned/future.

Q07 must mark all real Dominium generated outputs as deferred. If Harness compile is updated, it should report bridge target plans only and must not write Dominium files.

## Compatibility/Pinning Model

Q07 should add `bridges/dominium/compatibility.yaml`.

The record should:

- reference `aide.compat-baseline.v0`;
- reference Q06 version registry and generated manifest version;
- define the bridge baseline id, for example `aide.dominium-bridge.v0`;
- define the recommended near-term adoption mode as `pinned-managed-repo-layer`;
- require Dominium to pin an AIDE commit, reviewed bundle, or future release artifact before adoption;
- require review for pin changes;
- state that Q07 creates no separate incompatible version system;
- state that bridge pinning is AIDE-side metadata until a future Dominium repo task consumes it.

## Harness Validate/Doctor/Compile Bridge Behavior

Q07 may update Harness minimally.

`aide validate` may check:

- required bridge files exist;
- bridge metadata has expected anchors;
- XStack records say Dominium-local and strict;
- policy overlays contain stricter-than-AIDE posture;
- compatibility/pinning record references Q06 baseline;
- generated target expectations are metadata-only and deferred.

`aide doctor` may report:

- Dominium Bridge baseline status;
- missing bridge files or stale bridge metadata;
- next repair step;
- reminder that Dominium repo mutation is out of scope.

`aide compile` may report:

- Dominium Bridge target classes as a plan only;
- no real Dominium generated outputs;
- generated artifacts remain non-canonical.

No Q07 Harness change may add provider calls, model calls, external repo access, network access, Runtime behavior, or real generated Dominium outputs.

## Planned Deliverables

Q07 implementation should create or update:

- `docs/reference/dominium-bridge.md`
- `bridges/dominium/README.md`
- `bridges/dominium/bridge.yaml`
- `bridges/dominium/adoption.md`
- `bridges/dominium/validation.md`
- `bridges/dominium/compatibility.yaml`
- `bridges/dominium/xstack/README.md`
- `bridges/dominium/xstack/scope.md`
- `bridges/dominium/xstack/portable-mapping.yaml`
- `bridges/dominium/profiles/README.md`
- `bridges/dominium/profiles/dominium-xstack.profile.yaml`
- `bridges/dominium/policies/README.md`
- `bridges/dominium/policies/review-gates.yaml`
- `bridges/dominium/policies/proof-gates.yaml`
- `bridges/dominium/policies/generated-artifacts.yaml`
- `bridges/dominium/generators/README.md`
- `bridges/dominium/generators/targets.yaml`
- optional minimal Harness bridge checks under `core/harness/**`
- optional `.aide/components/**`, `.aide/commands/**`, `.aide/evals/**`, `.aide/compat/**`, or `.aide/generated/**` metadata only when required by the implementation and allowed by this plan
- reference/root docs listed in allowed paths
- Q07 queue status, ExecPlan updates, and evidence

Required Q07 evidence:

- `.aide/queue/Q07-dominium-bridge-baseline/evidence/changed-files.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/validation.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/bridge-policy.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/remaining-risks.md`

## Milestones

1. Re-read AGENTS, queue policy, Q04/Q05/Q06 reviews, Q03-Q06 outputs, current bridge skeleton, reference docs, decisions, and Q07 task packet.
2. Confirm Q04 is `passed`, Q05 review evidence records `PASS_WITH_NOTES`, and Q06 review evidence records `PASS_WITH_NOTES`.
3. Run baseline `py -3 scripts/aide validate`, `doctor`, `compile`, and `migrate`.
4. Update Q07 status to `running` only after confirming allowed paths.
5. Create bridge reference documentation and top-level bridge metadata.
6. Create XStack boundary records.
7. Create Dominium/XStack profile overlay.
8. Create strict policy overlays.
9. Create generated target expectation metadata.
10. Create compatibility/pinning record.
11. Add minimal Harness bridge checks only if needed and within this plan.
12. Update root/reference docs minimally.
13. Run validation, queue helpers, bridge file checks, diff checks, and allowed-path audit.
14. Write Q07 evidence.
15. Stop at `needs_review` or write blocker evidence if blocked.

## Progress

- 2026-04-30: Q07 plan-only packet created after Q06 review commit `c6a3e04 Review Q06 compatibility baseline`.
- 2026-04-30: Q07 planning accepted Q05 and Q06 `PASS_WITH_NOTES` review evidence as dependency gates while preserving the raw `needs_review` queue statuses to avoid generated manifest drift.
- 2026-04-30: Q07 planning chose `pinned-managed-repo-layer` as the recommended near-term Dominium adoption mode.
- 2026-04-30: Q07 planning chose an AIDE-side bridge metadata/profile/policy/generator/compatibility packet as the minimum bridge unit.
- 2026-04-30: No Q07 implementation, final bridge files, Dominium repo changes, Runtime, Hosts, provider integrations, generated Dominium outputs, or Q08+ work were created by this plan-only task.
- 2026-04-30: Q07 implementation began after re-reading AGENTS, queue policy/index, Q04-Q06 review evidence, Q07 task packet, Q03-Q06 outputs, current bridge skeleton, and root/reference docs.
- 2026-04-30: Baseline Harness checks before editing returned `PASS_WITH_WARNINGS` with expected review-gate and generated-manifest stale-source warnings, and no hard errors.
- 2026-04-30: Added AIDE-side Dominium Bridge records under `bridges/dominium/**`, including bridge metadata, adoption guidance, validation guidance, XStack scope/mapping, profile overlay, strict policies, generator target metadata, and compatibility pinning.
- 2026-04-30: Added `docs/reference/dominium-bridge.md` and updated source-of-truth, generated-artifact, compatibility, bridge charter, root documentation, planning, and implementation records.
- 2026-04-30: Added minimal Harness structural checks for required Dominium Bridge files and anchors, plus compile-plan reporting for Dominium target classes. The Harness does not mutate Dominium repos or emit real Dominium outputs.
- 2026-04-30: Updated bounded `.aide/components`, `.aide/commands`, and `.aide/evals` metadata for bridge posture.
- 2026-04-30: Q07 status moved to `needs_review`; no Q08, Runtime, Host, provider, release, external Dominium repo, or real generated Dominium output work was implemented.

## Surprises And Discoveries

- Q05 and Q06 review tasks intentionally left queue status/index unchanged because `.aide/queue/index.yaml` is part of the generated manifest source fingerprint. Q07 planning must rely on review evidence rather than raw status alone.
- Updating `.aide/queue/index.yaml` for Q07 planning will make the Q05 generated manifest source fingerprint stale until a future implementation task is allowed to refresh it with `aide compile --write`.
- `.aide/profile.yaml`, `.aide/policies/generated-artifacts.yaml`, and generated summaries still contain some stale Q05/Q06 wording. Q06 review records this as cleanup before Q08 or broader automation, not a Q07 planning blocker.
- Q07 implementation changed generated-artifact source inputs, so `.aide/generated/manifest.yaml` remains stale by source fingerprint. This is recorded as review-visible drift rather than refreshed because Q07 does not own Q05 generated artifact refresh.

## Decision Log

- 2026-04-30: Q07 planning may proceed from Q06 review outcome `PASS_WITH_NOTES`.
- 2026-04-30: The minimum bridge unit is metadata plus overlays plus generated-target expectations plus compatibility pinning plus validation declarations.
- 2026-04-30: Near-term Dominium adoption mode is `pinned-managed-repo-layer`, not template mode, bridge-pack mode, or release-bundle mode.
- 2026-04-30: XStack remains Dominium-local and strict; AIDE remains portable below it.
- 2026-04-30: Q07 does not create real Dominium generated outputs.
- 2026-04-30: Q07 does not modify the Dominium repo.
- 2026-04-30: Q07 compatibility/pinning should reference Q06 Compatibility baseline and should not create a separate incompatible version system.
- 2026-04-30: Q07 implements minimal Harness bridge checks because the bridge baseline should be enforceable enough for review, but those checks are structural and non-mutating only.
- 2026-04-30: Q07 does not run `aide compile --write`; generated summaries and `.aide/generated/manifest.yaml` drift are left as explicit review-visible state.

## Validation And Acceptance

This plan-only task is acceptable when:

- `.aide/queue/Q07-dominium-bridge-baseline/task.yaml` exists.
- `.aide/queue/Q07-dominium-bridge-baseline/ExecPlan.md` exists and contains all required sections.
- `.aide/queue/Q07-dominium-bridge-baseline/prompt.md` exists.
- `.aide/queue/Q07-dominium-bridge-baseline/status.yaml` exists.
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/planning-validation.md` exists.
- `.aide/queue/index.yaml` references Q07 task, ExecPlan, prompt, and evidence paths.
- Q04 passed status is confirmed.
- Q05 and Q06 accepted-equivalent review evidence is confirmed.
- Validation commands are recorded.
- No implementation work or forbidden paths are modified.

Q07 implementation will be acceptable only when:

- bridge docs and records define scope, XStack boundary, stack order, profile overlay, policy overlay, generated target expectations, and compatibility pinning;
- Harness bridge checks, if added, are structural and non-mutating;
- generated target expectations remain metadata-only;
- no Dominium repo or external path is modified;
- Q07 evidence is complete;
- Q07 stops at review.

Q07 implementation result:

- bridge docs and records were added;
- Harness bridge checks were added and remain structural/non-mutating;
- generated target expectations are metadata-only;
- no external Dominium repo path was modified;
- no real Dominium generated outputs were emitted;
- Q07 is stopped at `needs_review`.

## Idempotence And Recovery

A stateless worker can restart Q07 by reading:

- `AGENTS.md`
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- Q04, Q05, and Q06 review evidence
- Q03-Q06 outputs
- `.aide/profile.yaml`, `.aide/toolchain.lock`, `.aide/components/**`, `.aide/commands/**`, `.aide/evals/**`, `.aide/adapters/**`, `.aide/compat/**`
- `scripts/aide`, `core/harness/**`, `core/compat/**`
- `docs/reference/harness-v0.md`, `docs/reference/generated-artifacts-v0.md`, `docs/reference/compatibility-baseline.md`, `docs/reference/source-of-truth.md`
- current `bridges/dominium/**` skeleton docs
- `docs/decisions/ADR-0006-xstack-dominium-local.md`
- this Q07 `task.yaml`, `ExecPlan.md`, `prompt.md`, and `status.yaml`

If partial Q07 implementation exists, run `py -3 scripts/aide validate`, inspect `bridges/dominium/**`, inspect Q07 evidence, and confirm no external Dominium repo path was modified before editing. Preserve unrelated user changes. If a requested bridge change would require Dominium product semantics, Runtime, provider/model calls, or external repo mutation, stop and write blocker evidence.

## Evidence To Produce

Q07 implementation should produce:

- `.aide/queue/Q07-dominium-bridge-baseline/evidence/changed-files.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/validation.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/bridge-policy.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/remaining-risks.md`
- `.aide/queue/Q07-dominium-bridge-baseline/evidence/blocker.md` if blocked

The plan-only task produces:

- `.aide/queue/Q07-dominium-bridge-baseline/evidence/planning-validation.md`

## Outcomes And Retrospective

Plan-only outcome:

- Q07 is planned and ready for a future implementation worker.
- Q07 implementation remains pending and review-gated.
- No final bridge metadata, Dominium repo changes, Harness bridge checks, generated Dominium outputs, Runtime, Hosts, provider integrations, app surfaces, release automation, or autonomous service logic were implemented.
- Q08 self-hosting automation remains deferred.

Implementation outcome:

- Q07 Dominium Bridge baseline is implemented AIDE-side and awaiting review.
- XStack remains Dominium-local and strict.
- Dominium Bridge records map AIDE concepts to Dominium/XStack expectations without making AIDE Dominium-shaped.
- The bridge owns metadata, overlays, target expectations, validation posture, and compatibility pinning only.
- Real Dominium repo adoption, generated outputs, XStack proof execution, Runtime, Hosts, providers, app surfaces, release automation, and Q08 automation remain deferred.
