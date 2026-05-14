# Q42 Prompt Summary

Implement AIDE's deterministic Move Map / Salvage Map / Path Alias v0 planning
layer. The task requires candidate-only migration maps, salvage plans, path
alias plans, reference rewrite plans, and draft migration ledger events for
future refactor, root recycling, tool absorption, install, upgrade, and cleanup
work.

This packet intentionally stores a bounded prompt summary instead of raw prompt
history. Raw prompt execution, raw prompt logs, and raw response logs remain out
of scope.

## Required Boundary

- Candidate planning only.
- No file move, delete, rewrite, alias application, shim creation, target repo
  mutation, branch mutation, provider/model call, or network call.
- Generated current maps are evidence, not target truth.
