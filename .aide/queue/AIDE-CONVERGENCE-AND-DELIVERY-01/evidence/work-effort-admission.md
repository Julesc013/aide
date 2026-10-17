# Bounded whole-work effort observation

Prepared at clean integrated source a0970badeca5b3332505a4158fcfca6b075e07e3.
The previous engineering-review child is complete with verified dev/main receipt.
P5.observation and the existing next-briefs.md identify this independent consumer:
an operator must see failed attempts and unavailable accounting across the whole
workflow, without reconstructing several job documents or claiming child savings.

Existing owners: Lite job usage/receipt readers, core.execution managed receipts,
and the existing Codex attributed usage parser. ExecutionHostUsage is a separate
projection contract; this view will not redefine it or create a new authority.
Imported economics specifications remain proposed context, not execution grants.

Implement one read-only `job effort --work-set PATH` view. A finite manifest names
one work identity, explicit receipt paths/digests and their declared workflow
phase. All nine phases (preparation, context, execution, tests, review, repair,
integration, recovery, cleanup) remain visible, including unobserved phases.
Use existing bounded JSON/path checks; read only explicit contained repo-relative
ordinary inputs, refuse redirection/duplicates/malformed or mismatched identities.
At most16 receipt entries,64KiB manifest,256KiB each receipt, bounded output.
Do not discover sessions, scan unrelated files or follow receipt-owned paths.

Normalize actual managed receipts through a small pure module under existing
core.execution, lazily loaded by the CLI. Bind job/manifest/work/source identities,
retain failure/cancellation/incomplete outcomes and reconciliation state. Duplicate
same-job/same-bytes observations count once; conflicting snapshots or phase
attribution refuse rather than sum. Unknown receipt semantics remain explicit.
Single-job memory/scratch peak maxima are not aggregate host peaks or additive
costs. Retained collection hashes are observed metadata, not proof of revalidation.

Optionally reuse the existing Codex attempt-set importer for a pinned supplied
roster; bind its work identity and preserve cumulative/overlap/unknown semantics.
No new model counter parser, tariff engine or credential access. Missing streams,
controller/human time, complete coverage, accepted-outcome latency and currency
cost stay null/unknown. Observation never sets task acceptance or dispatches work.
Default compact human output and JSON expose the same facts and limitations.

Real consumer: summarize all five original engineering-review native attempts,
including both failures and the passing repairs/preview. Verify exact job identity,
three successful and two failed attempts, retirement observations and unknown
model/review/preparation coverage. Preserve originals, no rewriting of their data.
This demonstrates useful observation, not whole-outcome savings or a benchmark.

Allowed child paths:
- .aide/queue/AIDE-WORK-EFFORT-01/**
- core/execution/work_effort.py
- .aide/scripts/aide_lite.py (job view handler, lazy import, CLI and portable list)
- .aide/scripts/tests/test_work_effort.py
- docs/reference/aide-lite-test-runner.md
- .aide/commands/catalog.yaml (existing job command documentation if needed)
- .aide/queue/index.yaml
- parent ExecPlan.md/status.yaml and this admission record
- .aide/intake/latest-* and .aide/context/latest-task-packet.md
- .aide/reports/capability-* through the existing owner
- existing development export and six changelog previews through existing owners
- PLANS.md, IMPLEMENT.md, DOCUMENTATION.md

The existing test_efficiency_wait.py suite is read-only and all its methods remain
required. New tests cover positive/unknown/missing phases, failed/cancelled work,
identity conflicts and duplicate suppression, resource non-additivity, mismatched
work or digest, path/redirection/size/JSON refusals, actual human/JSON CLI behavior,
optional usage import and unchanged unknown/overlap semantics.

Maximum3 sequential managed allocations: source tests plus actual prior-work view;
changed portable export plus actual delivered checks; existing promotion preview.
Use one admitted finite route and fresh source/inputs/pause/reservation checks.
Failures consume allocations; no automatic retry. Exact independent review of
source/effect precedes every new qualification. Original bytes/results remain.
No prior model allowance renewed; no provider, installed-host, target, release,
secret, privilege, machine configuration, new root or protection changes.

After qualification and exact terminal review, use the standing delegation for
structured local commits, current-ref fetch, guarded dev/main fast-forward and
nonforce sync, post-dev validation and post-main preview verification. Create only
local task/aide-work-effort-01 in the existing checkout, classify the four owned
intake files before branch creation, and retire only that branch after confirmed
integration. No other branch publication/deletion or released-asset replacement.

Intake's lexical release/blocked/split result is preserved: excluded release words
trigger it. This bounded observation child is the explicit non-release split.
Pending installed-host binding and target ownership remain independent prerequisites
for their workflows, not permission to substitute these observations for them.
