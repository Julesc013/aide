# Future Worker Prompt For Q02

You are GPT-5.5 Codex working inside the existing `julesc013/aide` repository.

Process queue item `Q02-structural-skeleton` only. Do not implement Q03, Q04, Q05, Q06, Q07, Q08, or any later queue item.

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
6. Read `.aide/queue/Q02-structural-skeleton/task.yaml`.
7. Read `.aide/queue/Q02-structural-skeleton/ExecPlan.md`.
8. Read `.aide/queue/Q02-structural-skeleton/status.yaml`.
9. Read root docs: `README.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md`.
10. Inspect the current top-level repo tree and the major directories named in the ExecPlan.

If Q00 or Q01 is still `needs_review`, proceed only if the human prompt explicitly authorizes Q02 implementation after review consideration. Otherwise, record the dependency and stop.

Your job is to implement Q02 structural skeleton only. Create additive directories, README files, `docs/reference/structural-migration-map.md`, root doc pointers, and Q02 evidence. Preserve bootstrap-era history, phase records, source files, tests, imports, and host proof records. Prefer mapping over moving.

Update `ExecPlan.md` as a living document while you work. Record progress, discoveries, decisions, validation, and retrospective notes. Write evidence under `.aide/queue/Q02-structural-skeleton/evidence/`.

Stay inside the allowed paths in `task.yaml`. Do not modify forbidden paths. Do not move files. Do not refactor implementation code. Do not implement Runtime, Service, Commander, Mobile, IDE extensions, provider adapters, app surfaces, package/release automation, or Q03+ work.

Run proportionate validation, including queue scripts, required file checks, terminology checks, allowed-path audit, and lightweight import-preservation checks. Do not run heavy host/native tests. Record commands and results in evidence. When complete, set Q02 status to `needs_review`. If blocked, set it to `blocked` and write `.aide/queue/Q02-structural-skeleton/evidence/blocker.md`.
