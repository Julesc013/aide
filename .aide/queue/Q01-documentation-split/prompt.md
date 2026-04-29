# Future Worker Prompt For Q01

You are GPT-5.5 Codex working inside the existing `julesc013/aide` repository.

Process queue item `Q01-documentation-split` / `Q01-documentation-split-and-canonical-architecture` only. Do not implement Q02, Q03, Q04, or any later queue item.

Before editing:

1. Read `AGENTS.md`.
2. Read `.aide/queue/policy.yaml`.
3. Read `.aide/queue/index.yaml`.
4. Read `.aide/queue/Q00-bootstrap-audit/status.yaml`.
5. Read Q00 outputs:
   - `docs/constitution/bootstrap-era-aide.md`
   - `docs/charters/reboot-charter.md`
   - `docs/reference/repo-census.md`
   - `docs/roadmap/reboot-roadmap.md`
6. Read `.aide/queue/Q01-documentation-split/task.yaml`.
7. Read `.aide/queue/Q01-documentation-split/ExecPlan.md`.
8. Read `.aide/queue/Q01-documentation-split/status.yaml`.
9. Read root docs: `README.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md`.
10. Inspect existing documentation-like directories named in the ExecPlan.

If Q00 is still `needs_review`, proceed only if the human prompt explicitly authorizes Q01 implementation after review consideration. Otherwise, record the dependency and stop.

Your job is to implement Q01 documentation architecture only. Preserve bootstrap-era history, phase records, and evidence. Split documentation additively into the planned families. Link or map old documentation areas; do not move them.

Update `ExecPlan.md` as a living document while you work. Record progress, discoveries, decisions, validation, and retrospective notes. Write evidence under `.aide/queue/Q01-documentation-split/evidence/`.

Stay inside the allowed paths in `task.yaml`. Do not modify forbidden paths. Do not build Runtime, Hosts, Commander, Mobile, Visual Studio, Xcode, VS Code, provider adapters, app surfaces, packaging, release automation, or implementation code.

Run proportionate validation, including queue scripts and terminology checks. Record commands and results in evidence. When complete, set Q01 status to `needs_review`. If blocked, set it to `blocked` and write `.aide/queue/Q01-documentation-split/evidence/blocker.md`.
