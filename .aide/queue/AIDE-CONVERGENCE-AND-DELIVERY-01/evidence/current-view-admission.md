# AIDE-DAILY-CURRENT-VIEW-01 admission candidate

Parent: AIDE-CONVERGENCE-AND-DELIVERY-01. Base source753de2e3659b8828b6e779b4cb8397f8efc11099.
Authority: owner's active daily-use Goal and existing bounded-child delegation.
Existing reviewed brief: evidence/current-view-brief.md. This packet requests
bounded child admission, not source acceptance, remote integration or publication.

Objective: extend the existing `task current` read-only projection so an operator
or agent can select a native AIDE queue task and understand its objective, current
recorded outcome, scope, evidence availability, remaining obligations and next
responsible action without reconstructing historical reports. Retain existing
default selection and ID/status lines and exit behavior for valid current tasks.

Allowed child paths:

- .aide/queue/AIDE-DAILY-CURRENT-VIEW-01/**
- .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_task_binding.py
- .aide/scripts/tests/test_task_current.py
- .aide/scripts/tests/test_x_os_01_task_os_commands.py
- .aide/queue/index.yaml
- .aide/context/latest-task-packet.md
- .aide/generated/**
- .aide/reports/capability-*.json
- .aide/reports/capability-*.md
- .aide/verification/latest-verification-report.md
- .aide/queue/AIDE-CONVERGENCE-AND-DELIVERY-01/ExecPlan.md
- .aide/queue/AIDE-CONVERGENCE-AND-DELIVERY-01/status.yaml
- PLANS.md
- IMPLEMENT.md
- DOCUMENTATION.md
- docs/reference/task-packets.md

No production policy, schema-authority, export/archive, original assertion weakening,
target, provider, account, machine configuration, reserve, dependency installation,
new storage root, runtime/server, external messaging or remote-ref effects. Ordinary
source edits and necessary checks remain under existing authority; source acceptance
and each managed effect require exact independent review. No helper/module extraction.

Implementation: add optional `--task-id` and `--json` to existing `task current`.
Use one bounded projection for both renderings, existing identity/resolution owners,
and explicit provenance for selected fields. Read current status from status.yaml;
task.yaml declarations and queue-index projections do not silently supersede it.
Show contradictions among current observations. Parse only supported scalar/folded
text shapes; malformed/duplicate/unsupported fields become explicit unknown/issues.
Do not introduce a general YAML implementation or runtime dependency.

References are scoped, finite metadata observations, never evidence acceptance.
Refuse escaping identities and outside/private/link targets before reading them;
bound file reads, fields and output. Missing references remain visible, and supplied
digest mismatches are stale observations. Unchecked applicability stays unknown.
Never treat needs_review or output existence as accepted. One passed fixture may
still have unperformed native target adoption. Missing owner/next action is unknown.

Acceptance: default/explicit selection, stable JSON, concise equivalent human view,
complete fixture vs pending consumer obligations, malformed/duplicate/conflicting/
missing/unsafe/stale cases, and read-only before/after fixture snapshots. Preserve
all17existing task-binding tests and applicable Task OS checks. Record unknown
model/controller/review cost honestly. Live local read-only smoke uses the completed
DiskEd task; fixtures remain separate from full daily-use/platform claims.

Local task branch: task/aide-daily-current-view-01, existing checkout, after clean
helper plan and exact admission. Preserve the current branch and all pending local
commits; no reset, force, worktree creation or remote mutation.

Qualification placement: unchanged shared managed-workspace runner, Python3.14.8
SHA434b361fe0c5960d404974feed493db47f2603a1ace2574312104fbed0182c6f,
config61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90.
Maximum two jobs: focused qualification and one conditional affected repair only.
Existing limits/reserves (1GiB worker/180seconds) stay unchanged. Exact HEAD/tree,
source/test/import pins, pause/reservations and capacity rechecked under shared
admission; isolated controller. Owned temporary fixtures only, no model/network or
canonical job output. Retain streams/receipt/digests, reconcile uncertainty, prove
quiescence/scratch absence/reservation release. No retries of unchanged passed work.

Stop conditions: exact result or terminal prerequisite; preserve original failure
and gaps. Reconcile a changed subject before reuse. Two-job ceiling does not widen
itself. Independent tasks may continue. New release/support/model/target claims
need their own evidence and effects.
