# Future Worker Prompt For Q03

You are GPT-5.5 Codex working inside the existing `julesc013/aide` repository.

Process queue item `Q03-profile-contract-v0` only. Do not implement Q04, Q05, Q06, Q07, Q08, or any later queue item.

Before editing:

1. Read `AGENTS.md`.
2. Read `.aide/queue/policy.yaml`.
3. Read `.aide/queue/index.yaml`.
4. Read Q00 status, ExecPlan, evidence, and outputs:
   - `.aide/queue/Q00-bootstrap-audit/status.yaml`
   - `.aide/queue/Q00-bootstrap-audit/ExecPlan.md`
   - `docs/constitution/bootstrap-era-aide.md`
   - `docs/charters/reboot-charter.md`
   - `docs/reference/repo-census.md`
   - `docs/roadmap/reboot-roadmap.md`
5. Read Q01 status, ExecPlan, evidence, and outputs:
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
6. Read Q02 status, ExecPlan, evidence, and outputs:
   - `.aide/queue/Q02-structural-skeleton/status.yaml`
   - `.aide/queue/Q02-structural-skeleton/ExecPlan.md`
   - `core/README.md`
   - `core/contract/README.md`
   - `core/harness/README.md`
   - `core/compat/README.md`
   - `core/control/README.md`
   - `core/sdk/README.md`
   - `docs/reference/structural-migration-map.md`
7. Read `.aide/queue/Q03-profile-contract-v0/task.yaml`.
8. Read `.aide/queue/Q03-profile-contract-v0/ExecPlan.md`.
9. Read `.aide/queue/Q03-profile-contract-v0/status.yaml`.
10. Read root docs: `README.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md`.
11. Inspect current `.aide/**`, `.agents/**`, `scripts/**`, `core/contract/**`, and `docs/reference/**`.

If Q00, Q01, or Q02 is still `needs_review`, proceed only if the human prompt explicitly authorizes Q03 implementation after review consideration. Otherwise, record the dependency and stop.

Your job is to implement Q03 Profile/Contract v0 only. Define Profile as declarative repo contract, not executable machinery. Keep Harness distinct: Harness is later executable machinery for import, compile, validate, doctor, bakeoff, migrate, and drift checks.

Create or update only the files allowed by `task.yaml`. Preserve bootstrap-era history, phase records, source files, host proof lanes, eval records, packaging records, environment records, and evidence. Do not move source files. Do not implement Harness commands, generated downstream artifacts, Runtime, Hosts, Commander, Mobile, IDE extension families, provider adapters, app surfaces, or autonomous service logic. Do not implement Q04+.

Update `ExecPlan.md` as a living document while you work. Record progress, discoveries, decisions, validation, and retrospective notes. Write evidence under `.aide/queue/Q03-profile-contract-v0/evidence/`, including `changed-files.md`, `validation.md`, `profile-shape.md`, and `remaining-risks.md`.

Run proportionate validation, including queue scripts, required file checks, source-of-truth and terminology searches, allowed-path audit, and lightweight contract-shape checks. Do not run heavy host/native tests. Record commands and results in evidence. When complete, set Q03 status to `needs_review`. If blocked, set it to `blocked` and write `.aide/queue/Q03-profile-contract-v0/evidence/blocker.md`.
