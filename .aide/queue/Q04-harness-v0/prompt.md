# Future Worker Prompt: Q04 Harness v0

You are GPT-5.5 Codex working inside the existing `julesc013/aide` repository.

You are executing AIDE queue item:

`.aide/queue/Q04-harness-v0/`

This is the Q04 implementation task.

Your job is to implement the minimal AIDE Harness v0 described by the Q04 ExecPlan.

Do not implement Q05 or later work. Do not generate downstream target artifacts. Do not implement the full Compatibility baseline. Do not implement Dominium Bridge behavior. Do not build Runtime, Hosts, Commander, Mobile, Visual Studio/Xcode/VS Code extensions, provider adapters, app surfaces, or autonomous service logic.

Core doctrine:

- AIDE is being rebooted/refactored in place, not restarted from scratch.
- Preserve bootstrap-era history, phase records, source files, proofs, and evidence.
- Public model: AIDE Core, AIDE Hosts, AIDE Bridges.
- Internal Core split: Contract, Harness, Runtime, Compatibility, Control, SDK.
- First shipped stack: Contract + Harness + Compatibility + Dominium Bridge.
- XStack remains Dominium's strict local governance/proof profile.
- The filesystem queue under `.aide/queue/` is canonical.
- ExecPlans are the unit of long-running autonomous work.
- Q04 is Harness v0 implementation only.
- Profile/Contract is declarative repo truth from Q03.
- Harness is executable machinery for local import, compile, validate, doctor, migrate, and bakeoff checks.
- Generated downstream artifacts remain Q05.
- Compatibility baseline remains Q06.
- Dominium Bridge implementation remains Q07.

Before editing:

1. Read `AGENTS.md`.
2. Read `.aide/queue/policy.yaml`.
3. Read `.aide/queue/index.yaml`.
4. Read Q00 outputs if present:
   - `.aide/queue/Q00-bootstrap-audit/status.yaml`
   - `.aide/queue/Q00-bootstrap-audit/ExecPlan.md`
   - `docs/constitution/bootstrap-era-aide.md`
   - `docs/charters/reboot-charter.md`
   - `docs/reference/repo-census.md`
   - `docs/roadmap/reboot-roadmap.md`
5. Read Q01 outputs if present:
   - `.aide/queue/Q01-documentation-split/status.yaml`
   - `.aide/queue/Q01-documentation-split/ExecPlan.md`
   - `docs/charters/core-charter.md`
   - `docs/charters/contract-charter.md`
   - `docs/charters/harness-charter.md`
   - `docs/charters/compatibility-charter.md`
   - `docs/charters/hosts-charter.md`
   - `docs/charters/bridges-charter.md`
   - `docs/charters/control-charter.md`
   - `docs/charters/sdk-charter.md`
   - `docs/reference/documentation-migration-map.md`
6. Read Q02 outputs if present:
   - `.aide/queue/Q02-structural-skeleton/status.yaml`
   - `.aide/queue/Q02-structural-skeleton/ExecPlan.md`
   - `core/README.md`
   - `core/contract/README.md`
   - `core/harness/README.md`
   - `core/compat/README.md`
   - `core/control/README.md`
   - `core/sdk/README.md`
   - `docs/reference/structural-migration-map.md`
7. Read Q03 outputs if present:
   - `.aide/queue/Q03-profile-contract-v0/status.yaml`
   - `.aide/queue/Q03-profile-contract-v0/ExecPlan.md`
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
8. Read Q04 files:
   - `.aide/queue/Q04-harness-v0/task.yaml`
   - `.aide/queue/Q04-harness-v0/ExecPlan.md`
   - `.aide/queue/Q04-harness-v0/prompt.md`
   - `.aide/queue/Q04-harness-v0/status.yaml`
9. Read root docs:
   - `README.md`
   - `ROADMAP.md`
   - `PLANS.md`
   - `IMPLEMENT.md`
   - `DOCUMENTATION.md`
10. Inspect current `core/harness/**`, `core/contract/**`, `.aide/**`, `scripts/**`, `.agents/**`, and `docs/reference/**`.
11. Inspect existing queue scripts:
   - `scripts/aide-queue-next`
   - `scripts/aide-queue-status`
   - `scripts/aide-queue-run`
12. Do not assume Q00, Q01, Q02, or Q03 succeeded unless their files/status show that. If they remain `needs_review`, proceed only if the human prompt explicitly authorizes Q04 implementation or accepted reviews are present.
13. Treat the Q04 ExecPlan as authoritative. If it is incomplete, update it minimally before implementation and record the decision.

Allowed paths:

- `core/harness/**`
- `core/contract/**` only for read-only-compatible helpers or docs required by the Harness
- `scripts/aide`
- `scripts/**` only for small wrappers or test helpers directly needed for Harness v0
- `docs/reference/harness-v0.md`
- `docs/reference/profile-contract-v0.md` only if needed
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q04-harness-v0/**`
- `.aide/queue/index.yaml`

Forbidden paths:

- `shared/**`
- existing `hosts/**` implementation/proof files
- `bridges/**`
- `core/runtime/**`
- `core/compat/**` except conceptual docs references if needed
- `core/control/**` except conceptual docs references if needed
- `core/sdk/**`
- `governance/**`
- `inventory/**`
- `matrices/**`
- `research/**`
- `specs/**`
- `environments/**`
- `labs/**`
- `evals/**`
- `packaging/**`
- generated downstream artifacts such as `CLAUDE.md`, `.claude/**`, or final generated `.agents/skills/*` target outputs
- provider/model integrations
- runtime/broker/service code
- IDE/app/host code

Implementation requirements:

1. Implement a small repo-root Harness entrypoint, preferably `scripts/aide`, using Python standard library only.
2. Keep Harness logic under `core/harness/**`; avoid turning the wrapper into a large script.
3. Implement these commands with honest v0 behavior:
   - `aide init`
   - `aide import`
   - `aide compile`
   - `aide validate`
   - `aide doctor`
   - `aide migrate`
   - `aide bakeoff`
4. Make `aide validate` the primary hard-check command and return nonzero on error diagnostics.
5. Use a restricted structural/text reader for Q03 YAML records unless a future reviewed dependency decision says otherwise.
6. Do not add PyYAML or other external dependencies.
7. Do not create generated downstream artifacts; `aide compile` reports only a compile plan.
8. Do not implement a migration engine; `aide migrate` reports no-op baseline or missing records.
9. Do not call models, providers, network services, native host tools, IDEs, package managers, or external automation.
10. Update `.aide/queue/Q04-harness-v0/ExecPlan.md` as a living document.
11. Write Q04 evidence under `.aide/queue/Q04-harness-v0/evidence/`.
12. Do not implement Q05+.

Required Q04 evidence files:

- `.aide/queue/Q04-harness-v0/evidence/changed-files.md`
- `.aide/queue/Q04-harness-v0/evidence/validation.md`
- `.aide/queue/Q04-harness-v0/evidence/command-smoke.md`
- `.aide/queue/Q04-harness-v0/evidence/remaining-risks.md`

Validation requirements:

1. Verify the Q04 Harness entrypoint and implementation files exist.
2. Run command help smoke.
3. Run `aide validate` and record the result.
4. Run `aide doctor` smoke.
5. Run `aide compile` and confirm it reports a compile plan without creating generated artifacts.
6. Run `aide migrate` no-op smoke.
7. Run `aide bakeoff` smoke and confirm no provider/model calls are made.
8. Run lightweight standard-library tests if added.
9. Run `scripts/aide-queue-status` and `scripts/aide-queue-next` if available.
10. Run text searches for Profile, Harness, validate, doctor, compile plan, source of truth, generated, Compatibility, and Dominium Bridge.
11. Run `git diff --check`.
12. Run an allowed-path audit.
13. Record validation commands and results in `.aide/queue/Q04-harness-v0/evidence/validation.md`.

If blocked:

- Stop.
- Write `.aide/queue/Q04-harness-v0/evidence/blocker.md`.
- Set Q04 status to `blocked`.
- Explain exactly what prevented completion.

At the end, respond with:

1. Summary of created/updated files.
2. Validation commands run and results.
3. Any blockers or risks.
4. Whether Q04 is `passed`, `needs_review`, or `blocked`.
5. Recommended next prompt: Q05 plan.
