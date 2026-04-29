# AIDE Self-Bootstrap Reference

## Why This Bootstrap Exists

AIDE is being rebooted in place. The repository already contains bootstrap-era governance, research, phase records, shared-core implementation history, and first host-lane proof records. The self-bootstrap scaffold gives future agents a filesystem-native way to continue work without treating chat state or extension task queues as authoritative.

The bootstrap does not finish AIDE. It creates a minimal queue, policy set, and first ExecPlan so later work can proceed in bounded, reviewable steps.

## Filesystem Queue

The canonical queue lives under `.aide/queue/`.

- `index.yaml` records queue order.
- `policy.yaml` records state, evidence, and stop rules.
- Each task directory contains `task.yaml`, `ExecPlan.md`, `prompt.md`, `status.yaml`, and `evidence/`.

The Codex extension UI can launch or discuss work, but it is not canonical. If chat and the filesystem disagree, future agents should trust the filesystem and record the discrepancy in evidence.

## Using The Q00 Prompt

To start Q00, read `.aide/queue/Q00-bootstrap-audit/prompt.md` and follow it exactly. Q00 verifies and freezes baseline facts; it does not implement Q01 or any later item.

Useful local commands:

```powershell
py -3 scripts/aide-queue-status
py -3 scripts/aide-queue-next
py -3 scripts/aide-queue-run
```

`scripts/aide-queue-run` is a non-destructive skeleton. It prints the next task and prompt only.

## Continuing Future Work

Future agents should process one queue item at a time unless policy changes explicitly allow more concurrency. They should read the task packet, update status, maintain the ExecPlan, stay inside allowed paths, run validation, write evidence, and stop at blockers or review gates.

Q01 through Q04 are listed as planned queue items only. They need their own task packets and review before implementation.

## Queue-Driven Autonomy

"Do everything until done" becomes queue-driven autonomy in AIDE. Broad goals are decomposed into ExecPlans. Each ExecPlan has bounded scope, deterministic evidence, validation, and review gates. Fully autonomous work is still constrained by `.aide/queue/policy.yaml` and `.aide/policies/*.yaml`.

## What Remains Manual

- Human review of hard gates and completed queue items.
- Approval for permission widening, destructive operations, secret access, publishing, merge-to-main, and policy changes.
- Creation and review of future queue task packets.
- Real runtime, host, app, packaging, provider, and release work.

