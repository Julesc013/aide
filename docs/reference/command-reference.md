# AIDE Command Reference

## Status

Current status: partial.

## Current Commands

The current reboot command surface is limited to conservative queue helpers:

- `scripts/aide-queue-status`: summarizes queue item statuses.
- `scripts/aide-queue-next`: prints the next pending queue item.
- `scripts/aide-queue-run`: prints the next task and prompt; it does not invoke Codex or a worker.

## Deferred Commands

Future command references may cover Contract, Harness, Compatibility, generated-artifact, Dominium Bridge, or worker automation commands only after reviewed queue items create them. Q01 does not add new commands.
