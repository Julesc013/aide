# P0.current_view: next bounded preparation brief

Status: proposed, not admitted implementation. Parent: AIDE-CONVERGENCE-AND-DELIVERY-01.
Existing roadmap: P0.current_view, with P5 observation and P6 reuse as opportunities,
not hard programme dependencies. Useful consumers: the operator and an agent
resuming the completed DiskEd preparation without reopening its tests.

Problem: `command_task_current` in `.aide/scripts/aide_lite.py` exposes ID/status
only. Outcome boundaries, valid earlier evidence and the next responsible action
require reading several records. A passed preparation can be mistaken for completed
target adoption, and historical planning status can be mistaken for current state.

Proposed change: extend that existing read-only command with explicit named-task
selection and structured output, using the existing resolver/inspection/status
owners. Preserve existing task ID, status lines and exit behavior. Present a
bounded current summary: objective, current recorded status/result, acceptance
scope, evidence references, unresolved obligations, next action and responsible
owner when recorded. Missing data stays unknown. Reference evidence without
claiming that existence or an old PASS proves current applicability. Report
contradictory current fields explicitly; do not invent a universal chronological
winner or promote `needs_review` to accepted.

Implementation scope to propose in the child: existing CLI implementation and
parser; `.aide/scripts/tests/test_task_binding.py` and relevant Task OS tests;
affected command reference; child's queue/evidence/ExecPlan and normal scoped
indexes. No exporter/archive rebuild unless the resulting release or consumer
claim actually requires it. No broker, scheduler, daemon, network transport,
provider dependency, native target edit or status database.

Acceptance and verification:

- Default and explicit task selection preserve accepted identity/refusal rules.
- Human and JSON views derive from the same bounded projection. JSON has a stated
  version, deterministic ordering and explicit unknowns; human output is concise.
- Completed preparation with unperformed target adoption shows both facts.
- Missing, malformed, conflicting and stale references are visible without
  silently changing records or accepting work. Do not follow untrusted references
  outside the selected repository or display secrets/private state.
- A before/after source/fixture snapshot proves observation writes nothing.
- Targeted existing binding and Task OS checks remain valid; add meaningful
  expected-result fixtures for these new behaviors, not implementation mirrors.
- Record preparation, validation and review effort with unknown usage explicit.

Before implementation, create the bounded child through existing intake/queue
preparation, freeze allowed paths and exact candidate, and obtain the applicable
independent review. Success is one useful view with its refusal cases, not a new
task engine or completion of all P0/P6. No dependencies on mini, two agent backends,
Workbench, native target mutation or full ProjectGraph are required.
