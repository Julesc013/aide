---
type: AIDE Engineering Specification
title: Supervision, durable controls and continuity
description: Durable work matters more than an immortal process or connection.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P04
  resource: urn:aide:source-package:b3f3d0d27109a986e537928523c9c34f31e3458986c7632e97abee06d85db64c
  title: AIDE-Spec-Overhaul-2026-09-20(3)(1).zip
- id: P06
  resource: urn:aide:source-package:83f9926500c47e3ee8384868c7d4046083e2a75bef0d667fb526c8476446d121
  title: AIDE-Spec-Overhaul-2026-09-20-R2(2)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P20
  resource: urn:aide:source-package:90f79366cb02f34d737950db6708c087db367e36e7ce5ff98f7d953c6a82fb96
  title: AIDE-Specification-Overhaul-2026-09-20(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: coordinator
  applicability: continuous-worker profile
  requirement_ids:
  - UR-SUP-01
  - UR-SUP-02
  - UR-SUP-03
  - UR-SUP-04
  - UR-SUP-05
  - UR-SUP-06
  - UR-SUP-07
---

# Supervision, durable controls and continuity

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Durable work matters more than an immortal process or connection.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

The current continuous-worker source is an opt-in bounded prototype with real process and local ledger machinery; it is not an accepted unattended product. The proposed contract generalizes its intent-before-launch, exact candidate, independent-test, assurance and integration-observation discipline. Preserve existing activation formats and source pins until explicit versioned migration.

Pause-dispatch, drain, cancel-task, emergency-stop and resume have different meanings. Pause prevents the next dispatch without discarding the active result. Drain lets active work finish or reconcile, then claims no new work. Cancel requests termination of owned work and preserves its artifacts. Emergency-stop prevents new dispatch and stops owned local processes but cannot retroactively cancel an already submitted remote effect. Resume cannot erase cancellation or expand scope.

Use kernel or backend ownership tokens and fencing epochs, not stored PIDs, to control live processes. Locks protect shared mutable domains; they should not unnecessarily stop independent admitted tasks after a local blocker. Show why progress is waiting. Demonstrate two useful real tasks, independent verification, legitimate integration and observed closeout before claiming continuous productive autonomy. Fixture progression and synthetic sessions remain valuable but narrower evidence.

## Interface and data boundary

Programme; admitted task set; current attempt; owned process/job; lease epoch; control state; dependency readiness; checkpoint; verification; effect state; closeout.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-SUP-01 — Owned process control

Process termination and fencing MUST use independently established ownership rather than PID value alone.

### UR-SUP-02 — Durable control meanings

Pause, drain, cancel, emergency-stop and resume MUST have separate persisted semantics.

### UR-SUP-03 — Uncertain shared writer

An unresolved shared external effect MUST retain its writer/fencing protection while independent non-conflicting work may proceed.

### UR-SUP-04 — Independent continuity proof

Productive continuous-worker acceptance MUST require useful real tasks, actual verification and authoritative integration observation, not only synthetic progress.

### UR-SUP-05 — Current immutable activation

Attempts MUST bind exact activation/source/configuration versions and refuse material drift.

### UR-SUP-06 — Bounded waits

Waiting MUST use typed resume conditions and bounded polling/backoff without keeping a reasoning session active by default.

### UR-SUP-07 — Independent emergency path

Emergency control and evidence recovery MUST remain usable when the model, worker or optional UI fails.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-SUP-01` | A stored PID is reused by an unrelated process. | AIDE does not kill it as its own worker. |
| `UC-SUP-02` | Restart a paused coordinator with a completed active attempt. | It retains evidence and starts no new work until allowed. |
| `UC-SUP-03` | A merge request times out. | No conflicting writer starts, but unrelated admitted tasks may continue. |
| `UC-SUP-04` | A fake-model two-task test passes. | The result is fixture-qualified, not a live-pilot acceptance. |
| `UC-SUP-05` | Change the coordinator code during an active admitted run. | Continuation refuses or requires requalification rather than using old hashes as authority. |
| `UC-SUP-06` | A long test waits for an external result. | The controller persists the wait and no model polling loop runs. |
| `UC-SUP-07` | The worker hangs while the UI disconnects. | A qualified separate control path can stop owned local work and inspect retained state. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
