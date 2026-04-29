# Future Worker Prompt For Q00

You are GPT-5.5 Codex working inside the existing `julesc013/aide` repository.

Process queue item `Q00-bootstrap-audit` only. Do not implement Q01, Q02, Q03, Q04, or any later queue item.

Before editing:

1. Read `AGENTS.md`.
2. Read `.aide/queue/README.md`.
3. Read `.aide/queue/policy.yaml`.
4. Read `.aide/queue/Q00-bootstrap-audit/task.yaml`.
5. Read `.aide/queue/Q00-bootstrap-audit/ExecPlan.md`.
6. Read `.aide/queue/Q00-bootstrap-audit/status.yaml`.
7. Read `README.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md`.
8. Inspect the current repository structure and worktree status.

Your job is to verify and freeze the in-place reboot baseline. Preserve bootstrap-era phase history and evidence. Treat `.aide/queue/` as the canonical queue, not the Codex extension UI.

Update `ExecPlan.md` as a living document while you work. Record progress, discoveries, decisions, validation, and retrospective notes. Write evidence under `.aide/queue/Q00-bootstrap-audit/evidence/`.

Allowed paths are defined in `task.yaml`. Do not widen them silently. Do not modify forbidden paths. Stop at blockers and review gates.

Run proportionate validation, including the queue scripts if present. Record commands and results in evidence. When complete, set `status.yaml` to `needs_review`. If blocked, set it to `blocked` and write the blocker into evidence.

