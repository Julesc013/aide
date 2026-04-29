# ADR-0001: Reboot AIDE In Place

## Status

accepted

## Context

AIDE has bootstrap-era governance, architecture, implementation proofs, evidence, and blocker records. Restarting greenfield would hide that history and weaken auditability.

## Decision

Reboot AIDE in place. Preserve bootstrap-era phase records, documents, evidence, and blockers while refactoring future work through the filesystem queue.

## Consequences

- New architecture docs must map old records instead of deleting them.
- Claims must distinguish implemented reality from future intent.
- The repo remains pre-product until release and verification evidence changes that.

## Supersedes / Superseded By

Supersedes: none. Superseded by: none.
