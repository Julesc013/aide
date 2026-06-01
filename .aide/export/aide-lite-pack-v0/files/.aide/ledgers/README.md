# AIDE Task OS Ledgers

This directory contains append-only-style ledger schemas for Task OS v0.

The schemas define record shapes for task, blocker, capability, branch provenance, and checkpoint history. X-OS-00 does not create authoritative instance ledgers that claim current repo history. Example records live under `.aide/examples/task-os/` and are marked as examples.

X-OS-01 command outputs under `.aide/reports/task-os-*` are generated report evidence, not canonical append-only ledgers.
