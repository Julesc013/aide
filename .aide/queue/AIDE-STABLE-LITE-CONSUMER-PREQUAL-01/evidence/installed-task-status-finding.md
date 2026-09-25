# Installed target task status finding, 2026-09-25

## Reproduction and scope

- The target is a new disposable directory at
  `D:/Projects/AIDE/_review_scratch/stable-lite-context-probe/run-clean-20260925-2154/fresh-target`.
  It was imported from the exact local preview ZIP SHA-256
  `8c4fbef71470954c64dbd09e181384a3fbff0ec997a799ef197f0f6cce1e07f6`
  using its extracted CLI. The target has no queue WorkUnits, as intended for a
  fresh import.
- After a successful installed `context`, `pack --task "Disposable installed AIDE
  context evidence smoke task"`, and `verify` loop, the installed CLI's
  `task status` command exited 1. It printed `task_count: 0` and
  `latest_task_id: Q17`. The command log is external
  `stable-lite-context-probe/run-clean-20260925-2154/task-status.log`, SHA-256
  `d2bb16e19fd66b8437a88d2f454841f71e2dc04162d53ac1fe2ebb9c7882e81e`.
  The generated target report SHA-256 is
  `a4865f0b3835e6cd2f517db553998b31e128034202e02041e763cbb872cc033b`.
- The report explicitly marks `latest_task_packet_status: missing` and shows
  `selected_next_workunit: X-OS-01 - Task OS Report-Only Commands`, despite
  the empty target queue. No target task was run or admitted by this command.

## Likely cause and required disposition

`task_os_latest_task_ref` in the delivered `.aide/scripts/aide_lite.py`
searches the entire generated task packet after the `PHASE` and `GOAL`
sections. The generic task packet contains `Q17` only in contextual text
(`run route explain after Q17`), not as its phase or goal identity. The fallback
therefore promotes incidental context into a reported latest task. The
source-specific next-work selector also recommends X-OS-01 with an empty
target queue. `command_task_status` intentionally returns 1 when `tasks` is
empty; whether that exit convention should change requires a separate
contract decision.

This is a reproducible **report-truth finding**, not proof of unauthorized
execution or source-generated queue history in the target. The prequalification
WorkUnit owns read-only product source. Route any source change through a
bounded repair WorkUnit, add an empty-target regression, and repeat the
installed CLI check from regenerated reviewed bytes. Keep the present local
preview and failed status output as evidence; do not relabel it passing.
