# Correct the existing continuation recommendation

Baseline: 716ec1fd0ad6fb2d3875417c4db7b867a7b393fe, clean dev, previous child
integrated into local and remote dev/main. Intake is classified github/governance
because it includes subsequent integration; its behavior-proof split is retained.

Concrete defect: task resume-plan always prints safe_to_resume: true. Its report
points at X-OS-01 and recommends full validation regardless of the selected task.
This can mislead a restarting worker into replaying finished work or overlooking
uncertain effects. Existing task current already owns bounded task/status/evidence
observations; reuse it. No new checkpoint schema, task store or execution engine.

Child AIDE-RESUME-PLAN-01 will make the existing command describe the selected
WorkUnit's recorded outcome, owner, next action, obligations and evidence with
source references. Add --task-id and nonmutating --json. Preserve the legacy
human report-writing invocation and callable writer; label unknown readiness and
keep no-apply markers. A recommendation is not execution admission or acceptance.
Missing/conflicting records and evidence require reconciliation; blocked work
names its existing unblock condition; completed work directs inspection/reuse,
not automatic rerun. Running/failed attempts require reconciliation before retry.
Checks should follow changed subjects and dependencies; no blanket full rerun.
Independent authorized inspection remains possible without a new permission loop.

Scope: .aide/queue/AIDE-RESUME-PLAN-01/**; .aide/scripts/aide_lite.py (resume view,
handler, writer, parser and portable test membership); new tests/test_resume_plan.py
under .aide/scripts; docs/reference/task-os-report-only-commands.md; queue index;
parent ExecPlan.md/status.yaml and this admission; four current intake files;
latest-task-packet.md; existing capability reports; development export pack and
six changelog previews through existing owners; PLANS.md, IMPLEMENT.md,
DOCUMENTATION.md. Existing task-current, task-binding and X-OS-01 tests unchanged.

Acceptance: actual CLI JSON has no writes, stays on named identity even when the
latest packet changes, preserves original failed and completed records, marks
uncertain applicability and never authorizes effects. Legacy report generation
remains usable with dynamic task references and explicit readiness uncertainty.
An owned disposable consumer uses fresh processes to inspect an interrupted task
with one completed effect, retains the exact receipt and pending obligation, then
inspects the same identity after a recorded completion without replaying effects.
This qualifies continuation advice, not real host cancellation or runtime recovery.

Maximum3 sequential managed jobs: source checks plus ordinary CLI consumer;
existing exporter and actual delivered checks; existing fixed-range preview.
Failure consumes an allocation, no automatic retry. Each source/effect receives
exact independent review and fresh identity/pause/resource/ownership checks.
Resource policy unchanged. Reuse unaffected evidence; preserve every original
failure. No live models, providers, endpoints, target mutation, arbitrary desktop
control, spending, secrets, privilege/configuration/root changes or publication.

Use local task/aide-resume-plan-01 in this checkout after bounded admission review
and helper plan, classifying the four owned intake outputs and this record. With
qualified source, delivered artifact and terminal exact independent effect review,
use standing authorization for structured commits, nonforce dev/main sync with
fresh refs and shared ownership, post-dev validation, post-main fixed preview
verification, then retire only this fully integrated local branch. Do not publish
or prune unrelated branches. Published1.0.0 stays unchanged. Outstanding host and
DiskEd owner bindings remain separate unmet acceptance obligations.
