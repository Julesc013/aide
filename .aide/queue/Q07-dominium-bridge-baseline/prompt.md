# Q07 Dominium Bridge Baseline Implementation Prompt

You are GPT-5.5 Codex working inside the existing `julesc013/aide` repository.

You are executing AIDE queue item:

`.aide/queue/Q07-dominium-bridge-baseline/`

This is the Q07 Dominium Bridge baseline implementation task.

Do not implement Q08 or later work.
Do not modify any external Dominium repository.
Do not implement Dominium product/runtime semantics.
Do not implement Runtime, Hosts, Commander, Mobile, Visual Studio/Xcode/VS Code extensions, provider adapters, browser bridges, app surfaces, model calls, web search integrations, release automation, or autonomous service logic.
Do not emit real Dominium generated outputs.

Core doctrine:

- AIDE is being rebooted/refactored in place, not restarted from scratch.
- Preserve bootstrap-era history, phase records, and evidence.
- Public model: AIDE Core, AIDE Hosts, AIDE Bridges.
- Internal Core split: Contract, Harness, Runtime, Compatibility, Control, SDK.
- First shipped stack: Contract + Harness + Compatibility + Dominium Bridge.
- XStack remains Dominium's strict local governance/proof profile.
- AIDE remains the portable public repo-native operating layer.
- Bridges are downstream/project-specific overlays, not generic adapters.
- The filesystem queue under `.aide/queue/` is canonical.
- ExecPlans are the unit of long-running autonomous work.
- Profile / Contract is declarative repo truth.
- Harness is executable machinery over that truth.
- Generated downstream artifacts are compiled or managed outputs, not canonical truth.
- Compatibility governs evolution of AIDE repo contracts, generated artifacts, Harness metadata, queue records, and migrations.
- Q07 owns the Dominium Bridge baseline.

Before editing:

1. Read `AGENTS.md`.
2. Read `.aide/queue/policy.yaml`.
3. Read `.aide/queue/index.yaml`.
4. Confirm Q04 is `passed`.
5. Read Q04 review evidence:
   - `.aide/queue/Q04-harness-v0/evidence/review.md`
   - `.aide/queue/Q04-harness-v0/evidence/review-validation.md`
   - `.aide/queue/Q04-harness-v0/evidence/review-risks.md`
   - `.aide/queue/Q04-harness-v0/evidence/review-recommendation.md`
6. Read Q05 implementation and review evidence:
   - `.aide/queue/Q05-generated-artifacts-v0/ExecPlan.md`
   - `.aide/queue/Q05-generated-artifacts-v0/status.yaml`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review-validation.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review-risks.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review-recommendation.md`
7. Read Q06 implementation and review evidence:
   - `.aide/queue/Q06-compatibility-baseline/ExecPlan.md`
   - `.aide/queue/Q06-compatibility-baseline/status.yaml`
   - `.aide/queue/Q06-compatibility-baseline/evidence/review.md`
   - `.aide/queue/Q06-compatibility-baseline/evidence/review-validation.md`
   - `.aide/queue/Q06-compatibility-baseline/evidence/review-risks.md`
   - `.aide/queue/Q06-compatibility-baseline/evidence/review-recommendation.md`
8. Treat Q05 and Q06 `PASS_WITH_NOTES` review evidence as accepted-equivalent dependency gates if raw queue status still says `needs_review`; record that nuance in evidence.
9. Read Q03 contract files:
   - `.aide/profile.yaml`
   - `.aide/toolchain.lock`
   - `.aide/components/**`
   - `.aide/commands/**`
   - `.aide/policies/**`
   - `.aide/tasks/**`
   - `.aide/evals/**`
   - `.aide/adapters/**`
   - `.aide/compat/**`
   - `core/contract/**`
   - `docs/reference/profile-contract-v0.md`
   - `docs/reference/source-of-truth.md`
10. Read Q04/Q05/Q06 files:
    - `scripts/aide`
    - `core/harness/**`
    - `core/compat/**`
    - `docs/reference/harness-v0.md`
    - `docs/reference/generated-artifacts-v0.md`
    - `docs/reference/compatibility-baseline.md`
    - `.aide/generated/**`
11. Read current bridge skeleton:
    - `bridges/README.md`
    - `bridges/dominium/README.md`
    - `bridges/dominium/xstack/README.md`
    - `bridges/dominium/profiles/README.md`
    - `bridges/dominium/policies/README.md`
    - `bridges/dominium/generators/README.md`
12. Read:
    - `docs/charters/bridges-charter.md`
    - `docs/decisions/ADR-0006-xstack-dominium-local.md`
    - `docs/reference/structural-migration-map.md`
    - `docs/reference/documentation-migration-map.md`
    - `README.md`
    - `ROADMAP.md`
    - `PLANS.md`
    - `IMPLEMENT.md`
    - `DOCUMENTATION.md`
13. Read Q07 files:
    - `.aide/queue/Q07-dominium-bridge-baseline/task.yaml`
    - `.aide/queue/Q07-dominium-bridge-baseline/ExecPlan.md`
    - `.aide/queue/Q07-dominium-bridge-baseline/prompt.md`
    - `.aide/queue/Q07-dominium-bridge-baseline/status.yaml`
14. Run baseline checks:
    - `py -3 scripts/aide validate`
    - `py -3 scripts/aide doctor`
    - `py -3 scripts/aide compile`
    - `py -3 scripts/aide migrate`
15. Treat the Q07 ExecPlan as authoritative. If it is incomplete, contradictory, or unsafe, stop and write a blocker.

Allowed paths:

- `bridges/dominium/**`
- `core/harness/**` only for minimal bridge-aware validate/doctor/compile status checks described by the Q07 ExecPlan
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

Forbidden paths:

- any external Dominium repository path
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

Primary goal:

Implement the smallest enforceable AIDE-side Dominium Bridge baseline so Dominium can later consume AIDE as a pinned portable repo layer under XStack strict governance.

Implementation deliverables:

1. Create or update `docs/reference/dominium-bridge.md`.
2. Add minimal bridge metadata and guidance under `bridges/dominium/**`.
3. Add XStack boundary records that keep XStack Dominium-local.
4. Add a Dominium/XStack profile overlay that does not replace `.aide/profile.yaml`.
5. Add strict policy overlays that do not weaken AIDE base policies.
6. Add generator target metadata only; do not emit real Dominium outputs.
7. Add compatibility/pinning records that reference Q06 Compatibility baseline.
8. Add minimal Harness validate/doctor/compile bridge checks only if needed and explicitly described by the ExecPlan.
9. Update docs/root indexes minimally.
10. Update Q07 `status.yaml` and `ExecPlan.md` as living documents.
11. Write evidence under `.aide/queue/Q07-dominium-bridge-baseline/evidence/`.

Required evidence files:

- `changed-files.md`
- `validation.md`
- `bridge-policy.md`
- `remaining-risks.md`

Validation requirements:

1. Run pre-change:
   - `py -3 scripts/aide validate`
   - `py -3 scripts/aide doctor`
   - `py -3 scripts/aide compile`
   - `py -3 scripts/aide migrate`
2. Run post-change:
   - `py -3 scripts/aide validate`
   - `py -3 scripts/aide doctor`
   - `py -3 scripts/aide compile --dry-run`
   - `py -3 scripts/aide migrate`
3. Run lightweight Harness tests if Q07 updates Harness checks.
4. Run bridge file existence and anchor checks.
5. Run queue helper scripts.
6. Run generated artifact drift checks and record whether index or source-input changes stale `.aide/generated/manifest.yaml`.
7. Run `git diff --check`.
8. Run an allowed-path audit.
9. Do not run heavy host/native tests, network calls, provider/model calls, browser tests, packaging/release automation, external Dominium repo commands, or anything requiring secrets.

Acceptance criteria:

- Dominium Bridge docs and records exist.
- XStack is explicitly Dominium-local and strict.
- Profile overlay exists and does not replace the AIDE Profile.
- Policy overlays are stricter than AIDE base policy.
- Generated target expectations are metadata-only and no real Dominium outputs are emitted.
- Compatibility/pinning references Q06 baseline and does not create a separate version system.
- Harness bridge checks, if added, are structural and non-mutating.
- Q07 evidence is complete.
- No forbidden paths were modified.
- No Q08+ implementation was performed.
- No Runtime, Host, provider, app, release, or service implementation was added.

If blocked:

- Stop.
- Write `.aide/queue/Q07-dominium-bridge-baseline/evidence/blocker.md`.
- Set Q07 status to `blocked`.
- Explain exactly what prevented completion.

At the end, respond with:

1. Summary of created/updated files.
2. Validation commands run and results.
3. Any blockers or risks.
4. Whether Q07 is `passed`, `needs_review`, or `blocked`.
5. Recommended next prompt: Q07 review, or QFIX if blocked.
