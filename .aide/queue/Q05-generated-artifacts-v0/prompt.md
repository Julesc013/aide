# Future Worker Prompt: Q05 Generated Artifacts v0

You are GPT-5.5 Codex working inside the existing `julesc013/aide` repository.

You are executing AIDE queue item:

`.aide/queue/Q05-generated-artifacts-v0/`

This is the Q05 implementation task.

Your job is to implement the minimal generated downstream artifact v0 pipeline described by the Q05 ExecPlan.

Do not implement Q06 or later work. Do not implement the full Compatibility baseline. Do not implement Dominium Bridge behavior. Do not build Runtime, Hosts, Commander, Mobile, Visual Studio/Xcode/VS Code extensions, provider adapters, model calls, browser bridges, web portals, app surfaces, release automation, or autonomous service logic.

Core doctrine:

- AIDE is being rebooted/refactored in place, not restarted from scratch.
- Preserve bootstrap-era history, phase records, source files, proofs, and evidence.
- Public model: AIDE Core, AIDE Hosts, AIDE Bridges.
- Internal Core split: Contract, Harness, Runtime, Compatibility, Control, SDK.
- First shipped stack: Contract + Harness + Compatibility + Dominium Bridge.
- XStack remains Dominium's strict local governance/proof profile.
- The filesystem queue under `.aide/queue/` is canonical.
- ExecPlans are the unit of long-running autonomous work.
- Profile/Contract is declarative repo truth from Q03.
- Harness is executable machinery from Q04.
- Generated downstream artifacts are outputs, not canonical truth.
- Q05 owns generated downstream artifacts v0.
- Compatibility baseline remains Q06.
- Dominium Bridge implementation remains Q07.

Before editing:

1. Read `AGENTS.md`.
2. Read `.aide/queue/policy.yaml`.
3. Read `.aide/queue/index.yaml`.
4. Read Q04 review evidence:
   - `.aide/queue/Q04-harness-v0/evidence/review.md`
   - `.aide/queue/Q04-harness-v0/evidence/review-validation.md`
   - `.aide/queue/Q04-harness-v0/evidence/review-risks.md`
   - `.aide/queue/Q04-harness-v0/evidence/review-recommendation.md`
5. Read Q04 implementation evidence:
   - `.aide/queue/Q04-harness-v0/evidence/changed-files.md`
   - `.aide/queue/Q04-harness-v0/evidence/validation.md`
   - `.aide/queue/Q04-harness-v0/evidence/command-smoke.md`
   - `.aide/queue/Q04-harness-v0/evidence/remaining-risks.md`
6. Read the foundation review and full audit:
   - `.aide/queue/foundation-review/foundation-review.md`
   - `.aide/queue/foundation-review/q05-readiness.md`
   - `.aide/queue/full-audit/audit-report.md`
   - `.aide/queue/full-audit/q05-blocker-review.md`
   - `.aide/queue/full-audit/planning-recommendations.md`
7. Read Q00 through Q04 outputs and evidence as needed.
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
9. Read Q04 Harness files:
   - `scripts/aide`
   - `core/harness/**`
   - `docs/reference/harness-v0.md`
10. Read Q05 files:
   - `.aide/queue/Q05-generated-artifacts-v0/task.yaml`
   - `.aide/queue/Q05-generated-artifacts-v0/ExecPlan.md`
   - `.aide/queue/Q05-generated-artifacts-v0/prompt.md`
   - `.aide/queue/Q05-generated-artifacts-v0/status.yaml`
11. Read root docs:
   - `README.md`
   - `ROADMAP.md`
   - `PLANS.md`
   - `IMPLEMENT.md`
   - `DOCUMENTATION.md`
12. Inspect current agent-facing surfaces:
   - `AGENTS.md`
   - `.agents/**`
   - `CLAUDE.md` if present
   - `.claude/**` if present
   - existing generated-artifact markers if present
13. Confirm Q04 is `passed` in `.aide/queue/index.yaml`. If Q04 is not `passed`, stop and write a Q05 blocker.

Before generation:

1. Run `py -3 scripts/aide validate`.
2. Run `py -3 scripts/aide doctor`.
3. Run `py -3 scripts/aide compile`.
4. Record the baseline command results in Q05 evidence or the ExecPlan.

Implementation requirements:

1. Keep the Q05 ExecPlan as a living document.
2. Update Q05 status as work moves through `running`, `blocked`, or `needs_review`.
3. First perform the bounded Q03-era Harness wording refresh described by the ExecPlan.
4. Implement deterministic generated artifact markers and a manifest.
5. Update Harness compile/validate behavior for Q05 generated artifacts.
6. Use managed sections for `AGENTS.md` and the existing `aide-queue`, `aide-execplan`, and `aide-review` skills.
7. Keep `CLAUDE.md` preview-only unless the ExecPlan and evidence explicitly justify final emission.
8. Keep `.claude/settings.json` deferred in Q05 v0.
9. Keep `.claude/agents/**` preview-only if emitted.
10. Do not silently overwrite manual content.
11. Run Harness validation after generation.
12. Write Q05 evidence.
13. Do not implement Q06+.

Required Q05 evidence files:

- `.aide/queue/Q05-generated-artifacts-v0/evidence/changed-files.md`
- `.aide/queue/Q05-generated-artifacts-v0/evidence/validation.md`
- `.aide/queue/Q05-generated-artifacts-v0/evidence/generated-artifact-policy.md`
- `.aide/queue/Q05-generated-artifacts-v0/evidence/remaining-risks.md`

Validation requirements:

1. Run `py -3 scripts/aide validate` before generation.
2. Run `py -3 scripts/aide doctor` before generation.
3. Run `py -3 scripts/aide compile` or its Q05 dry-run mode before writing targets.
4. Run generated preview/write commands according to the ExecPlan.
5. Run `py -3 scripts/aide validate` after generation.
6. Run lightweight Harness tests if Harness files changed.
7. Run `py -3 scripts/aide-queue-status`.
8. Run `py -3 scripts/aide-queue-next`.
9. Verify generated marker and manifest coherence.
10. Verify `CLAUDE.md` and `.claude/**` final targets match the Q05 target policy.
11. Run `git diff --check`.
12. Run an allowed-path audit.
13. Record commands and results in `.aide/queue/Q05-generated-artifacts-v0/evidence/validation.md`.

If blocked:

- Stop.
- Write `.aide/queue/Q05-generated-artifacts-v0/evidence/blocker.md`.
- Set Q05 status to `blocked`.
- Explain exactly what prevented completion.

At the end, respond with:

1. Summary of created/updated files.
2. Validation commands run and results.
3. Any blockers or risks.
4. Whether Q05 is `passed`, `needs_review`, or `blocked`.
5. Recommended next prompt: Q05 review, then Q06 plan only if Q05 passes.
