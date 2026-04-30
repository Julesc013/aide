# Q08 Implementation Prompt: Self-Hosting Automation

You are GPT-5.5 Codex working inside the existing `julesc013/aide` repository.

You are executing AIDE queue item:

`.aide/queue/Q08-self-hosting-automation/`

This is the Q08 self-hosting automation implementation task.

Do not implement Q09 or later work.
Do not implement Runtime, Hosts, Commander, Mobile, Visual Studio/Xcode/VS Code extensions, provider adapters, browser bridges, app surfaces, model calls, web search integrations, external CI, release automation, auto-merge, or autonomous service logic.
Do not invoke Codex or any external agent automatically.
Do not refresh generated artifacts unless a separate reviewed generated-artifact task explicitly authorizes it.

## Core Doctrine

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
- Q08 owns self-hosting automation scaffolding.
- Runtime, Hosts, Commander, Mobile, IDE extensions, pack/workflow IR, and provider/runtime adapters are later.

## Before Editing

1. Read `AGENTS.md`.
2. Read `.aide/queue/policy.yaml`.
3. Read `.aide/queue/index.yaml`.
4. Confirm Q04 and Q07 are `passed`.
5. Confirm Q05 and Q06 are accepted through review evidence even if raw status remains `needs_review`.
6. Read Q04 review evidence:
   - `.aide/queue/Q04-harness-v0/evidence/review.md`
   - `.aide/queue/Q04-harness-v0/evidence/review-validation.md`
   - `.aide/queue/Q04-harness-v0/evidence/review-risks.md`
   - `.aide/queue/Q04-harness-v0/evidence/review-recommendation.md`
7. Read Q05 review evidence:
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review-validation.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review-risks.md`
   - `.aide/queue/Q05-generated-artifacts-v0/evidence/review-recommendation.md`
8. Read Q06 review evidence:
   - `.aide/queue/Q06-compatibility-baseline/evidence/review.md`
   - `.aide/queue/Q06-compatibility-baseline/evidence/review-validation.md`
   - `.aide/queue/Q06-compatibility-baseline/evidence/review-risks.md`
   - `.aide/queue/Q06-compatibility-baseline/evidence/review-recommendation.md`
9. Read Q07 review evidence:
   - `.aide/queue/Q07-dominium-bridge-baseline/evidence/review.md`
   - `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-validation.md`
   - `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-risks.md`
   - `.aide/queue/Q07-dominium-bridge-baseline/evidence/review-recommendation.md`
10. Read Q03-Q07 outputs, including:
   - `.aide/profile.yaml`
   - `.aide/toolchain.lock`
   - `.aide/commands/**`
   - `.aide/policies/**`
   - `.aide/tasks/**`
   - `.aide/evals/**`
   - `.aide/compat/**`
   - `.aide/generated/**`
   - `scripts/aide`
   - `scripts/aide-queue-next`
   - `scripts/aide-queue-status`
   - `scripts/aide-queue-run`
   - `core/harness/**`
   - `core/compat/**`
   - `bridges/dominium/**`
   - `docs/reference/harness-v0.md`
   - `docs/reference/generated-artifacts-v0.md`
   - `docs/reference/compatibility-baseline.md`
   - `docs/reference/dominium-bridge.md`
   - `docs/reference/source-of-truth.md`
   - `docs/reference/self-bootstrap.md`
11. Read Q08 files:
   - `.aide/queue/Q08-self-hosting-automation/task.yaml`
   - `.aide/queue/Q08-self-hosting-automation/ExecPlan.md`
   - `.aide/queue/Q08-self-hosting-automation/prompt.md`
   - `.aide/queue/Q08-self-hosting-automation/status.yaml`
12. Read root docs:
   - `README.md`
   - `ROADMAP.md`
   - `PLANS.md`
   - `IMPLEMENT.md`
   - `DOCUMENTATION.md`
13. Run baseline checks before editing:
   - `py -3 scripts/aide validate`
   - `py -3 scripts/aide doctor`
   - `py -3 scripts/aide compile --dry-run`
   - `py -3 scripts/aide migrate`
   - `py -3 scripts/aide bakeoff`
   - `py -3 scripts/aide-queue-status`
   - `py -3 scripts/aide-queue-next`
14. Treat the Q08 ExecPlan as authoritative. If it is incomplete, contradictory, or unsafe, stop and write a blocker.

## Allowed Paths

- `scripts/aide`
- `scripts/aide-queue-run`
- `scripts/aide-queue-next` only if needed for read-only status correctness described by the Q08 plan
- `scripts/aide-queue-status` only if needed for read-only status correctness described by the Q08 plan
- `core/harness/**` only for safe self-check, doctor, queue-status, and audit behavior described by the Q08 plan
- `.aide/tasks/**` only if needed for self-hosting task declarations
- `.aide/policies/**` only if needed for stricter automation policy, not weakening existing gates
- `.aide/evals/**` only if needed for self-check or audit eval declarations
- `.aide/generated/**` only to read or report stale generated manifest state, not refresh unless a separate reviewed generated-artifact task authorizes it
- `.aide/runs/**` only for non-canonical self-check reports
- `docs/reference/self-hosting-automation.md`
- `docs/reference/self-bootstrap.md`
- `docs/reference/harness-v0.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/compatibility-baseline.md`
- `docs/reference/dominium-bridge.md`
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q08-self-hosting-automation/**`
- `.aide/queue/index.yaml`

## Forbidden Paths And Work

- Do not modify `shared/**`.
- Do not modify existing `hosts/**` implementation/proof files.
- Do not modify `bridges/**` except documentation links if needed; do not change Dominium Bridge implementation.
- Do not modify `core/runtime/**`, `core/control/**`, or `core/sdk/**` except conceptual documentation references if explicitly needed.
- Do not modify `governance/**`, `inventory/**`, `matrices/**`, `research/**`, `specs/**`, `environments/**`, `labs/**`, `evals/**` outside `.aide/evals/**`, or `packaging/**`.
- Do not implement provider/model integrations, web search integrations, local model integrations, runtime/broker/service code, IDE/app/host code, release/package automation, external CI automation, real external agent invocation, automatic Codex invocation, or queue auto-merge behavior.
- Do not refresh generated artifacts unless a separate reviewed generated-artifact task authorizes it.
- Do not implement Q09 or later work.

## Primary Goal

Implement safe self-hosting automation scaffolding so AIDE can inspect and report queue health, drift, doctor status, compile dry-run state, compatibility posture, bridge status, and proposed follow-up work while keeping all mutation and autonomy review-gated.

## Implementation Requirements

1. Create or update `docs/reference/self-hosting-automation.md`.
2. Add a bounded `py -3 scripts/aide self-check` command.
3. Keep self-check local, deterministic, standard-library only, report-first, and non-mutating by default.
4. If report writing is implemented, require an explicit flag and write only under `.aide/runs/self-check/**`.
5. Improve `scripts/aide-queue-run` only as a safe prompt/status helper. It must not invoke Codex or any external agent.
6. Fix stale `aide doctor` next-step wording in the smallest safe way.
7. Report stale generated manifest source fingerprint honestly and do not refresh generated artifacts automatically.
8. Report Q00-Q03/Q05/Q06 raw status and accepted review-evidence nuance separately.
9. Update the Q08 ExecPlan as a living document.
10. Write required Q08 evidence:
    - `.aide/queue/Q08-self-hosting-automation/evidence/changed-files.md`
    - `.aide/queue/Q08-self-hosting-automation/evidence/validation.md`
    - `.aide/queue/Q08-self-hosting-automation/evidence/automation-policy.md`
    - `.aide/queue/Q08-self-hosting-automation/evidence/self-check-output.md`
    - `.aide/queue/Q08-self-hosting-automation/evidence/remaining-risks.md`
11. Set Q08 status honestly, usually `needs_review` if implementation completes.

## Validation Requirements

Run and record:

- `py -3 scripts/aide validate`
- `py -3 scripts/aide doctor`
- `py -3 scripts/aide compile --dry-run`
- `py -3 scripts/aide migrate`
- `py -3 scripts/aide bakeoff`
- `py -3 scripts/aide self-check`
- report-write smoke if implemented
- `py -3 scripts/aide-queue-status`
- `py -3 scripts/aide-queue-next`
- `py -3 scripts/aide-queue-run`
- relevant Harness unittests
- `py -3 -m py_compile core/harness/*.py scripts/aide scripts/aide-queue-run scripts/aide-queue-next scripts/aide-queue-status`
- `git diff --check`
- allowed-path audit

Do not run heavy host/native tests, external provider/model calls, browser tests, network calls, packaging/release automation, external CI, or anything requiring secrets.

## Acceptance Criteria

- Self-hosting reference documentation exists.
- Self-check command exists and is report-first.
- Self-check reports queue health, generated drift, compatibility posture, bridge status, and follow-up recommendations without mutating canonical files by default.
- Queue runner remains non-destructive and does not invoke agents automatically.
- Doctor next-step wording no longer points to Q07 review after Q07 passed.
- Generated manifest staleness remains visible unless a separate reviewed generated-artifact task refreshes it.
- Evidence is complete.
- No forbidden paths or post-Q08 features are modified or implemented.

## If Blocked

Stop. Write `.aide/queue/Q08-self-hosting-automation/evidence/blocker.md`, set status to `blocked`, and explain exactly what prevented completion.

At the end, respond with:

1. Summary of created/updated files.
2. Validation commands run and results.
3. Self-hosting automation model implemented.
4. Any blockers or risks.
5. Whether Q08 is `passed`, `needs_review`, or `blocked`.
6. Recommended next prompt: Q08 review, or QFIX if blocked.
