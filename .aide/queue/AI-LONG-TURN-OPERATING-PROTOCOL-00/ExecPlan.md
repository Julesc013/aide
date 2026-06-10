# AI-LONG-TURN-OPERATING-PROTOCOL-00 ExecPlan

## Objective

Create a repo-local protocol for long-running AIDE and Codex queued turns. The
protocol must make multi-step work restartable, evidence-backed, and explicit
about stop conditions while staying docs-only.

## Scope

Allowed edits are limited to the paths listed in `task.yaml`: task-local queue
records and evidence, latest intake artifacts, `docs/planning/ai_long_turn_protocol/**`,
and the root planning, implementation, and documentation indexes.

## Non-Goals

- Do not change runtime behavior.
- Do not create, merge, promote, push, delete, or prune branches.
- Do not publish releases, create tags, upload artifacts, or change public
  readiness posture.
- Do not mutate target repositories.
- Do not call providers, models, Gateway surfaces, or network services.
- Do not run external discovery or fabricate external evidence.

## Current Facts To Verify

- The live branch at intake was `main...origin/main`.
- The current queue packet before this task pointed at
  `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`, not the pasted Eureka/dev
  state.
- The first raw intent compile of the attached prompt was blocked because the
  prompt mixed docs guidance with branch and release-class language.
- The safe split is docs-only and uses the hash recorded in
  `.aide/intake/latest-intent-packet.md`.

## Milestones

- [x] Inspect repository and queue state before editing.
- [x] Compile the raw request through AIDE intake.
- [x] Split the request to a safe docs-only WorkUnit.
- [x] Create queue packet and evidence scaffold.
- [x] Add long-turn protocol docs and templates.
- [x] Update documentation, planning, and implementation indexes.
- [x] Run validation and record final results.
- [ ] Commit the completed docs-only WorkUnit if validation passes.

## Decisions

- The requested `docs/planning/ai_long_turn_protocol/` path is preserved because
  the user supplied it explicitly, even though AIDE also uses `PLANS.md` for
  execution tracking and `docs/reference/` for many reference topics.
- The protocol talks about branch-sensitive and publication-sensitive work only
  as stop conditions and report fields. It does not authorize those actions.
- The stale pasted `dev` and product evidence state is treated as advisory
  context only. Live AIDE repo state controls this WorkUnit.

## Validation Intent

Run proportionate structural validation:

- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py intent validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AI-LONG-TURN-OPERATING-PROTOCOL-00`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AI-LONG-TURN-OPERATING-PROTOCOL-00`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`

If a command refreshes generated reports outside the task allowlist, restore
that incidental drift unless it becomes required evidence.

## Evidence

Evidence is written under
`.aide/queue/AI-LONG-TURN-OPERATING-PROTOCOL-00/evidence/`.

## Validation Results

- `git diff --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py intent validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AI-LONG-TURN-OPERATING-PROTOCOL-00`: PASS; classified complete with no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AI-LONG-TURN-OPERATING-PROTOCOL-00`: PASS; evidence files found.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- Requested Eureka-specific helper scripts are not present in this AIDE repo and were not run.

## Idempotence And Recovery

If interrupted, resume from `status.yaml`, this ExecPlan, the docs directory,
and the evidence files. Do not replay the raw pasted report as truth; rerun
intent compile or inspect `.aide/intake/latest-*` if intake evidence is needed.
