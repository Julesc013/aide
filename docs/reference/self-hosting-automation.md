# Self-Hosting Automation

## Purpose

Q08 adds the first safe self-hosting automation scaffold for AIDE. It lets AIDE inspect its own queue, validation, generated-artifact drift, Compatibility baseline, and Dominium Bridge posture without becoming an autonomous runtime or external worker launcher.

The automation is report-first. It can summarize state, write non-canonical self-check reports, and point to follow-up work. It does not merge, invoke Codex, call models, call providers, access the network, refresh generated artifacts, or mutate release state.

## Scope

Q08 covers:

- `aide self-check` as a local report command;
- deterministic self-check reports under `.aide/runs/self-check/` when explicitly requested;
- clearer `scripts/aide-queue-run` output for the next queue action and review-gate posture;
- a narrow `aide doctor` recommendation fix so it follows Q08 status instead of stale Q07 review guidance;
- documentation and evidence for known carry-forward issues.

## Allowed Automation

Q08 automation may:

- read `.aide/**`, `.aide/queue/**`, `.aide/generated/**`, `core/harness/**`, `core/compat/**`, and bridge metadata;
- run local structural checks through Harness code paths;
- report queue health and review-gate nuance;
- report generated manifest source-fingerprint drift;
- report Compatibility and Dominium Bridge smoke posture;
- write deterministic non-canonical self-check reports only when `--write-report` is provided.

## Forbidden Automation

Q08 automation may not:

- invoke Codex, Claude, OpenHands, external workers, models, providers, browsers, or network services;
- auto-merge, auto-commit, push, release, package, or run CI;
- silently refresh generated artifacts or `.aide/generated/manifest.yaml`;
- mutate core policy, Compatibility records, bridge records, generated outputs, or queue history outside the current reviewed task;
- run indefinitely or act as Runtime, Service, Commander, scheduler, broker, or host adapter.

## Evidence Outputs

Self-check reports are non-canonical evidence. The default report path is:

- `.aide/runs/self-check/latest.md`

The report contains no wall-clock timestamp. It is deterministic for a given repository state and records that it is not source of truth. Canonical truth remains in `.aide/`, `.aide/queue/`, compatibility records, generated-artifact manifests, bridge records, and reviewed queue evidence.

## Queue Proposal Rules

Q08 does not create new queue task packets automatically. It lists proposed follow-up work in self-check output only.

Any later task-generation behavior must be reviewed before use and must create proposed tasks in a review-gated state. Proposed tasks must include allowed paths, forbidden paths, validation requirements, and evidence requirements before execution.

## Review Gates

Self-hosting automation must respect existing gates:

- completed queue work stops at `needs_review`;
- accepted review evidence may allow later planning to proceed with notes, but raw queue status nuance remains visible;
- generated artifact drift requires a reviewed generated-artifact refresh task;
- policy, compatibility, bridge, and release changes require explicit reviewed queue work.

## Relationship To Runtime, Service, And Commander

Q08 is not Runtime, Service, Commander, or an autonomous scheduler. It is a local inspection and reporting layer over the existing Harness. Future Runtime or Commander work must treat Q08 reports as evidence, not as commands to execute automatically.

## Relationship To Agents

Codex and other agents remain workers. They may read self-check reports, but the reports do not replace queue prompts, ExecPlans, or human review. `scripts/aide-queue-run` prints the next queue action and prompt path; it does not start any agent.

## Carry-Forward Issues

Q08 handles current known issues as follows:

- stale `.aide/generated/manifest.yaml` source fingerprint: reported only; refresh is deferred to a reviewed generated-artifact QFIX;
- stale doctor output pointing to Q07 review: fixed narrowly by making the next recommendation follow Q08 status;
- Q00-Q03, Q05, and Q06 review-gated raw statuses: reported as nuance, not rewritten;
- Q03-era planned/not-implemented wording in some contract metadata: reported as cleanup candidate, not changed by Q08.
