# Q06 Compatibility Baseline Implementation Prompt

You are GPT-5.5 Codex working inside the existing `julesc013/aide` repository.

You are executing AIDE queue item:

`.aide/queue/Q06-compatibility-baseline/`

This is the Q06 Compatibility baseline implementation task.

Do not implement Q07 or later work.
Do not implement Dominium Bridge.
Do not implement Runtime, Hosts, Commander, Mobile, Visual Studio/Xcode/VS Code extensions, provider adapters, browser bridges, app surfaces, model calls, web search integrations, release automation, or autonomous service logic.
Do not build a full migration platform.
Do not alter generated artifact behavior.

Core doctrine:

- AIDE is being rebooted/refactored in place, not restarted from scratch.
- Preserve bootstrap-era history, phase records, and evidence.
- Public model: AIDE Core, AIDE Hosts, AIDE Bridges.
- Internal Core split: Contract, Harness, Runtime, Compatibility, Control, SDK.
- First shipped stack: Contract + Harness + Compatibility + Dominium Bridge.
- XStack remains Dominium's strict local governance/proof profile.
- The filesystem queue under `.aide/queue/` is canonical.
- ExecPlans are the unit of long-running autonomous work.
- Profile / Contract is declarative repo truth.
- Harness is executable machinery over that truth.
- Generated downstream artifacts are compiled or managed outputs, not canonical truth.
- Q06 owns the first real Compatibility baseline.
- Q07 owns the Dominium Bridge.

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
   - `.aide/queue/Q05-generated-artifacts-v0/task.yaml`
   - `.aide/queue/Q05-generated-artifacts-v0/ExecPlan.md`
   - `.aide/queue/Q05-generated-artifacts-v0/status.yaml`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/changed-files.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/validation.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/generated-artifact-policy.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/drift-check.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/remaining-risks.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review-validation.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review-risks.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review-recommendation.md`
7. Treat Q05 `PASS_WITH_NOTES` review evidence as the accepted-equivalent dependency gate if raw queue status still says `needs_review`; record that nuance in evidence.
8. Read Q03 contract files:
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
9. Read Q04/Q05 Harness and generated-artifact files:
   - `scripts/aide`
   - `core/harness/**`
   - `docs/reference/harness-v0.md`
   - `docs/reference/generated-artifacts-v0.md`
   - `.aide/generated/**`
10. Read current Compatibility skeleton:
    - `core/compat/**`
    - `.aide/compat/**`
    - `docs/charters/compatibility-charter.md`
11. Read Q06 files:
    - `.aide/queue/Q06-compatibility-baseline/task.yaml`
    - `.aide/queue/Q06-compatibility-baseline/ExecPlan.md`
    - `.aide/queue/Q06-compatibility-baseline/prompt.md`
    - `.aide/queue/Q06-compatibility-baseline/status.yaml`
12. Read root docs:
    - `README.md`
    - `ROADMAP.md`
    - `PLANS.md`
    - `IMPLEMENT.md`
    - `DOCUMENTATION.md`
13. Run baseline checks:
    - `py -3 scripts/aide validate`
    - `py -3 scripts/aide doctor`
    - `py -3 scripts/aide compile --dry-run`
    - `py -3 scripts/aide migrate`
14. Treat the Q06 ExecPlan as authoritative. If it is incomplete, contradictory, or unsafe, stop and write a blocker.

Allowed paths:

- `core/compat/**`
- `core/harness/**` only for migrate/validate compatibility checks
- `core/contract/**` only if needed for version metadata or docs
- `.aide/compat/**`
- `.aide/toolchain.lock` only for compatibility version alignment
- `.aide/generated/**` only to record/check the Q05 generated manifest version or refresh existing Q05 outputs if Q06 source-input edits make refresh unavoidable and evidence-backed
- `.aide/commands/**` only if needed to update migrate/validate compatibility status metadata
- `.aide/evals/**` only if needed for compatibility/replay declarations
- `docs/reference/compatibility-baseline.md`
- `docs/reference/profile-contract-v0.md`
- `docs/reference/harness-v0.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/source-of-truth.md`
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q06-compatibility-baseline/**`
- `.aide/queue/index.yaml`

Forbidden paths:

- `shared/**`
- existing `hosts/**` implementation/proof files
- `bridges/**`
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
- `evals/**` except specifically allowed AIDE compatibility/replay declarations under `.aide/evals/**`
- `packaging/**`
- `.aide/policies/**` unless a future prompt explicitly expands scope for generated-artifact policy cleanup
- provider/model integrations
- web search integrations
- local model integrations
- runtime/broker/service code
- IDE/app/host code
- release/package automation
- Q07/Q08 implementation

Primary goal:

Implement the smallest enforceable Compatibility baseline for AIDE repo evolution surfaces without overbuilding migration machinery.

Implementation deliverables:

1. Create or update `docs/reference/compatibility-baseline.md`.
2. Add small `core/compat/**` compatibility helpers or data-only equivalents using Python standard library only.
3. Add or update `.aide/compat/schema-versions.yaml`, `migration-baseline.yaml`, `replay-corpus.yaml`, `upgrade-gates.yaml`, and `deprecations.yaml`.
4. Update `.aide/toolchain.lock` only if needed for compatibility version alignment.
5. Update `aide migrate` so it reports compatibility baseline, current versions, available no-op migrations, and unknown-version posture without mutating files.
6. Update `aide validate` so it checks required compatibility records and known v0 versions, including generated manifest version if present.
7. Add a tiny replay baseline that checks deterministic Harness summaries, not Runtime behavior.
8. Add lightweight standard-library tests.
9. Update docs/root indexes minimally.
10. Update Q06 `status.yaml` and `ExecPlan.md` as living documents.
11. Write evidence under `.aide/queue/Q06-compatibility-baseline/evidence/`.

Required evidence files:

- `changed-files.md`
- `validation.md`
- `compatibility-policy.md`
- `replay-baseline.md`
- `remaining-risks.md`

Validation requirements:

1. Run pre-change:
   - `py -3 scripts/aide validate`
   - `py -3 scripts/aide doctor`
   - `py -3 scripts/aide compile --dry-run`
   - `py -3 scripts/aide migrate`
2. Run post-change:
   - `py -3 scripts/aide validate`
   - `py -3 scripts/aide doctor`
   - `py -3 scripts/aide compile --dry-run`
   - `py -3 scripts/aide migrate`
   - `py -3 scripts/aide bakeoff`
3. Run lightweight compatibility/Harness tests added by Q06.
4. Run `py -3 -m py_compile` over changed Python files.
5. Run queue helper scripts.
6. Run compatibility record checks and replay baseline checks.
7. Run `git diff --check`.
8. Run an allowed-path audit.
9. Do not run heavy host/native tests, network calls, provider/model calls, browser tests, packaging/release automation, or anything requiring secrets.

Acceptance criteria:

- Compatibility baseline docs and records exist.
- Supported v0 versions are explicit.
- Migration registry exists and is no-op-safe.
- Replay baseline is cheap, deterministic, and not Runtime replay.
- Upgrade gates and deprecation records exist.
- Harness `validate` and `migrate` report compatibility posture honestly.
- Unknown future versions are safe and actionable.
- Generated artifacts remain non-canonical.
- Q06 queue status and evidence are updated.
- No forbidden paths were modified.
- No Q07+ implementation was performed.

If blocked:

- Stop.
- Write `.aide/queue/Q06-compatibility-baseline/evidence/blocker.md`.
- Set Q06 status to `blocked`.
- Explain exactly what prevented completion.

At the end, respond with:

1. Summary of created/updated files.
2. Validation commands run and results.
3. Any blockers or risks.
4. Whether Q06 is `passed`, `needs_review`, or `blocked`.
5. Recommended next prompt: Q06 review, or QFIX if blocked.
