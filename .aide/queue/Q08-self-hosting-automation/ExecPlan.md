# Q08 ExecPlan: Self-Hosting Automation

## Purpose

Q08 will implement the first safe self-hosting automation scaffold for AIDE.

The goal is operational discipline, not autonomy theater. Q08 should let AIDE inspect itself, report queue and drift state, run safe local checks, and recommend follow-up work while preserving review gates and keeping `.aide/` plus `.aide/queue/` as canonical truth.

Q08 must not implement Runtime, Service, Commander, Hosts, Mobile, IDE extensions, providers, browser bridges, app surfaces, external CI, release automation, auto-merge, external model calls, web search, or uncontrolled autonomous worker execution.

## Background And Current Repo Context

AIDE is being rebooted in place. Bootstrap-era governance, inventory, matrices, research, shared-core implementation, host proof lanes, environments, evals, packaging records, and evidence remain visible.

Current facts verified during Q08 planning:

- Q04 Harness v0 is implemented and accepted with `PASS_WITH_NOTES`.
- Q05 generated artifacts v0 is implemented and reviewed with `PASS_WITH_NOTES`; its raw queue status remains `needs_review`.
- Q06 Compatibility baseline is implemented and reviewed with `PASS_WITH_NOTES`; its raw queue status remains `needs_review`.
- Q07 Dominium Bridge baseline is implemented and reviewed with `PASS_WITH_NOTES`; `.aide/queue/index.yaml` records Q07 as `passed`.
- `py -3 scripts/aide validate` exits `0` with `PASS_WITH_WARNINGS`.
- Current warnings include Q00-Q03 review gates, raw Q05/Q06 review gates, and stale Q05 generated manifest source fingerprint.
- `py -3 scripts/aide doctor` still prints `next_recommended_step: Q07 review...` even after Q07 passed. Q08 should fix or avoid relying on this stale guidance before automation treats doctor output as an execution signal.
- `py -3 scripts/aide compile --dry-run` reports `.aide/generated/manifest.yaml` as `would_replace` because the queue index changed after the last generated-artifact write.
- `scripts/aide-queue-run` is currently a non-destructive skeleton that prints the next pending task and prompt path; it does not invoke Codex or mutate files.

The future Q08 worker must re-read governing files and rerun baseline checks before editing.

## Scope

Q08 implementation should:

- create `docs/reference/self-hosting-automation.md`;
- add a bounded `aide self-check` command under the existing Harness command surface;
- keep self-check local, deterministic, standard-library only, and report-first;
- report queue health, review-gate nuance, generated artifact drift, compatibility status, Dominium Bridge status, and recommended follow-up work;
- optionally support an explicit `--write-report` or `--output` mode that writes non-canonical reports under `.aide/runs/self-check/**`;
- improve `scripts/aide-queue-run` as a safe read-only runner helper that refuses review-gate bypass and never launches agents automatically;
- fix stale `aide doctor` next-step wording in a bounded way so Q08 automation does not consume obsolete guidance;
- add minimal self-hosting task/policy/eval declarations only if needed and only if they strengthen review boundaries;
- update self-bootstrap, Harness, generated-artifact, compatibility, Dominium Bridge, and root docs minimally;
- write Q08 evidence and stop at review.

## Non-goals

- Do not implement Runtime, Service, Commander, Mobile, Hosts, IDE extensions, providers, browser bridges, app surfaces, external CI, release automation, packaging automation, or autonomous service logic.
- Do not invoke Codex, Claude, OpenHands, other external agents, models, providers, network services, or web search.
- Do not auto-merge, auto-commit, auto-approve, or bypass review gates.
- Do not silently refresh generated artifacts.
- Do not mutate `.aide/profile.yaml`, compatibility records, bridge files, generated artifacts, or root policy records except where explicitly allowed by this plan.
- Do not create real Q09 or later task packets.
- Do not rewrite Q00-Q03, Q05, or Q06 statuses as a hidden cleanup.
- Do not delete, move, or collapse bootstrap-era records.

## Allowed Paths For Q08 Implementation

- `scripts/aide`
- `scripts/aide-queue-run`
- `scripts/aide-queue-next` only if needed for read-only status correctness described by this plan
- `scripts/aide-queue-status` only if needed for read-only status correctness described by this plan
- `core/harness/**` only for safe self-check, doctor, queue-status, and audit behavior described by this plan
- `.aide/tasks/**` only if needed for self-hosting task declarations
- `.aide/policies/**` only if needed for stricter automation policy, not weakening existing gates
- `.aide/evals/**` only if needed for self-check or audit eval declarations
- `.aide/generated/**` only to read or report stale generated manifest state, not refresh unless a separate reviewed generated-artifact task authorizes it
- `.aide/runs/**` only for non-canonical self-check reports
- `docs/reference/self-hosting-automation.md`
- `docs/reference/self-bootstrap.md`
- `docs/reference/harness-v0.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/compatibility-baseline.md`
- `docs/reference/dominium-bridge.md`
- `README.md`
- `DOCUMENTATION.md`
- `ROADMAP.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `.aide/queue/Q08-self-hosting-automation/**`
- `.aide/queue/index.yaml`

## Forbidden Paths For Q08 Implementation

- `shared/**`
- existing `hosts/**` implementation/proof files
- `bridges/**` except documentation links if needed; do not change Dominium Bridge implementation
- `core/runtime/**`
- `core/control/**` except conceptual documentation references if needed
- `core/sdk/**`
- `governance/**`
- `inventory/**`
- `matrices/**`
- `research/**`
- `specs/**`
- `environments/**`
- `labs/**`
- `evals/**` except specifically allowed AIDE self-check declarations under `.aide/evals/**`
- `packaging/**`
- provider/model integrations
- web search integrations
- local model integrations
- runtime/broker/service code
- IDE/app/host code
- release/package automation
- external CI automation
- real external agent invocation
- automatic Codex invocation
- queue auto-merge behavior
- generated artifact refresh unless a separate reviewed generated-artifact task authorizes it
- Q09 or later implementation

## Self-Hosting Automation Model

At Q08, self-hosting automation means local repo inspection and review-gated recommendations.

Q08 should implement one primary Harness command:

```powershell
py -3 scripts/aide self-check
```

The command should gather a deterministic report from existing local records:

- current queue index and task status posture;
- accepted review evidence for Q04 through Q07;
- raw status/review-evidence nuance for Q00-Q03, Q05, and Q06;
- Harness validation summary;
- doctor summary and next-step sanity;
- compile dry-run generated-artifact state;
- compatibility migrate summary;
- Dominium Bridge structural status;
- known carry-forward risks;
- recommended follow-up tasks or prompts.

The command must not:

- invoke external agents;
- run network/model/provider calls;
- create or rewrite queue task packets by default;
- refresh generated artifacts;
- mutate compatibility or bridge records;
- treat generated reports as canonical truth.

## Automation Permission Model

Allowed by default:

- read local files;
- run structural in-process checks equivalent to Harness validate/doctor/compile dry-run/migrate summaries;
- print a report to stdout;
- classify findings as info, warning, review-required, or error;
- recommend follow-up prompts.

Allowed only with an explicit flag:

- write a non-canonical self-check report under `.aide/runs/self-check/**`.

Forbidden in Q08:

- automatic queue item execution;
- automatic queue item creation in `.aide/queue/**`;
- automatic Codex or model invocation;
- generated artifact refresh;
- mutating migrations;
- policy weakening;
- auto-commit, auto-merge, release, packaging, external CI, or publish actions.

## Queue Runner Model

Q08 should improve `scripts/aide-queue-run` conservatively.

Minimum behavior:

- read `.aide/queue/index.yaml`;
- print the next pending queue item;
- print task, ExecPlan, prompt, status, and evidence paths when available;
- report dependency/review-gate caveats when a task depends on accepted review evidence rather than raw `passed` status;
- refuse or warn clearly if a requested task would bypass an unresolved hard review gate;
- never invoke Codex, Claude, OpenHands, external models, shell-supplied arbitrary agent commands, or network tools.

The runner may print a manual next-command suggestion, but it must make clear that a human or explicit agent prompt starts the work.

## Evidence/Report Output Model

Default self-check output is stdout only.

If explicit report writing is implemented, use `.aide/runs/self-check/` as the non-canonical report path. Suggested files:

- `.aide/runs/self-check/latest.md`
- `.aide/runs/self-check/latest.yaml`

Do not use volatile timestamps in report contents unless the plan is updated with a deterministic policy. A stable `latest` file is enough for Q08.

Reports must state:

- `.aide/` remains canonical for Profile/Contract;
- `.aide/queue/` remains canonical for queue execution state;
- generated artifacts and self-check reports are outputs, not truth;
- recommended follow-ups are proposals, not automatically executable tasks.

## Proposed-Task Model

Q08 should not create executable queue task packets automatically.

The self-check report may include proposed follow-up prompt text or task outlines for:

- refreshing stale generated artifacts through a reviewed generated-artifact task;
- reconciling raw queue statuses after accepted review evidence;
- fixing stale documentation or command summaries;
- improving queue dependency awareness.

Actual task packet creation remains manual or future reviewed work. This avoids turning Q08 into an autonomous task generator before policy and review gates can support it.

## Known Carry-Forward Issues

Q08 must explicitly handle these current issues:

- `.aide/generated/manifest.yaml` is stale by source fingerprint after Q07 changed generated-artifact source inputs.
- `aide doctor` still recommends Q07 review even though Q07 passed.
- Q00-Q03 remain raw `needs_review` while foundation and later evidence accepted proceeding.
- Q05 and Q06 remain raw `needs_review` even though review evidence records `PASS_WITH_NOTES`.
- `scripts/aide-queue-next` is status-only and does not understand dependency review evidence.

## Drift/Status Reconciliation Plan

Generated manifest staleness:

- Q08 reports it as review-required drift.
- Q08 may run or summarize `compile --dry-run`.
- Q08 must not run `compile --write` unless a separate reviewed generated-artifact refresh task authorizes it.
- Q08 should recommend a small generated-artifact refresh QFIX after Q08 review if the drift remains.

Stale doctor output:

- Q08 may update doctor next-step logic as a bounded Harness fix.
- The fix should prefer canonical queue/index state plus review evidence over hard-coded Q07 guidance.
- The fix must not become a broad Harness refactor.

Raw status nuance:

- Q08 self-check should report raw queue state and accepted review-evidence state separately.
- Q08 should not rewrite Q00-Q03/Q05/Q06 statuses silently.
- Q08 may recommend a status reconciliation QFIX if future automation needs a cleaner status model.

Queue helper dependency awareness:

- Q08 may improve read-only queue helper summaries.
- It must not introduce automatic execution.

## Planned Deliverables

Q08 implementation should create or update:

- `docs/reference/self-hosting-automation.md`
- `docs/reference/self-bootstrap.md`
- `docs/reference/harness-v0.md`
- `docs/reference/generated-artifacts-v0.md`
- `docs/reference/compatibility-baseline.md`
- `docs/reference/dominium-bridge.md`
- `scripts/aide`
- `scripts/aide-queue-run`
- `core/harness/**` for self-check and bounded doctor/queue reporting
- optional `.aide/tasks/**`, `.aide/policies/**`, or `.aide/evals/**` records if needed for strict automation policy
- optional `.aide/runs/self-check/**` report output generated by an explicit self-check write mode
- root docs as needed
- Q08 status, ExecPlan, and evidence files

Required Q08 evidence:

- `.aide/queue/Q08-self-hosting-automation/evidence/changed-files.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/validation.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/automation-policy.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/self-check-output.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/remaining-risks.md`

## Milestones

1. Re-read governing docs, Q04-Q07 reviews, Q03-Q07 implementation outputs, current Harness/Compatibility/Bridge files, and this Q08 task packet.
2. Run baseline checks: validate, doctor, compile dry-run, migrate, bakeoff, queue status, and queue next.
3. Implement `docs/reference/self-hosting-automation.md`.
4. Add `aide self-check` with stdout report-first behavior.
5. Add explicit non-canonical report writing only if still small and deterministic.
6. Fix doctor next-step wording in the smallest safe way.
7. Improve `scripts/aide-queue-run` without adding automatic agent invocation.
8. Add lightweight tests for self-check and queue helper behavior where practical.
9. Update docs and task metadata.
10. Run validation, record evidence, set Q08 to `needs_review`, and stop.

## Progress

- [x] Q08 planning packet created.
- [x] Dependency and baseline validation recorded for plan-only work.
- [ ] Q08 implementation not started.
- [ ] Q08 evidence not produced beyond planning validation.
- [ ] Q08 review not started.

## Surprises And Discoveries

- `aide validate` currently passes with warnings only, even with stale generated manifest source fingerprint.
- `aide doctor` still reports Q07 review as next after Q07 has passed. This is not a planning blocker, but it must be fixed or bypassed before automation depends on doctor output.
- `scripts/aide-queue-next` reports Q08 as pending based on raw status only; it is intentionally not dependency-aware yet.

## Decision Log

- Q08 will use `aide self-check` as the smallest primary automation command instead of adding a new automation service or standalone runner.
- Q08 will keep `scripts/aide-queue-run` as a non-destructive helper and will not invoke Codex automatically.
- Q08 will not create executable proposed queue task packets. It may print recommended follow-up prompts in self-check reports.
- Q08 will not refresh stale Q05 generated artifacts automatically. It will report drift and recommend a reviewed generated-artifact QFIX if needed.
- Q08 may include a bounded doctor next-step fix because stale doctor guidance is unsafe as an automation signal.

## Validation And Acceptance

Implementation validation must include:

- `py -3 scripts/aide validate`
- `py -3 scripts/aide doctor`
- `py -3 scripts/aide compile --dry-run`
- `py -3 scripts/aide migrate`
- `py -3 scripts/aide bakeoff`
- `py -3 scripts/aide self-check`
- report-write smoke if implemented
- `py -3 scripts/aide-queue-status`
- `py -3 scripts/aide-queue-next`
- `py -3 scripts/aide-queue-run`
- relevant Harness unittests
- `py -3 -m py_compile core/harness/*.py scripts/aide scripts/aide-queue-run scripts/aide-queue-next scripts/aide-queue-status`
- `git diff --check`
- allowed-path audit

Q08 can be marked `needs_review` only when:

- self-check is local, deterministic, standard-library only, and report-first;
- no external agents or model/provider/network calls exist;
- generated artifacts are not silently refreshed;
- queue runner remains non-destructive;
- doctor next-step output is no longer stale or self-check avoids relying on it;
- evidence is complete;
- no forbidden paths are modified.

## Idempotence And Recovery

Self-check stdout must be deterministic for the same repository state.

If report writing is implemented, rerunning the command should replace only the selected non-canonical report file under `.aide/runs/self-check/**`.

If validation finds stale generated artifacts, Q08 should report the condition rather than repair it.

If a queue/status reconciliation issue is found, Q08 should recommend the smallest QFIX rather than rewriting queue history.

If the implementation would require external agents, network, runtime services, or generated artifact refresh, stop and write a blocker.

## Evidence To Produce

The Q08 worker must write:

- `changed-files.md`
- `validation.md`
- `automation-policy.md`
- `self-check-output.md`
- `remaining-risks.md`

Evidence should explicitly say whether:

- generated manifest drift remains;
- doctor next-step wording was fixed;
- queue-runner behavior remains non-mutating;
- self-check report writing, if present, is non-canonical;
- any proposed follow-up tasks were printed only and not added to `.aide/queue/**`.

## Outcomes And Retrospective

Q08 is not implemented by this planning task.

After implementation, record:

- what automation surface was added;
- what it can and cannot write;
- how generated artifact drift is reported;
- whether stale doctor output is fixed;
- what remains for future Runtime/Service/Commander work;
- whether Q08 can proceed to review.
