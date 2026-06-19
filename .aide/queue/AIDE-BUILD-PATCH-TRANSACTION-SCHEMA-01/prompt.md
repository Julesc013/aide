# Prompt: AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01

Create and process `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`.

Build the first minimal, portable, deterministic, schema-only
`PatchTransaction` protocol slice. A PatchTransaction represents a proposed,
bounded repository mutation that can be inspected, validated structurally,
linked to evidence, and reviewed before any apply operation exists.

Required outputs:

- schema
- helper/model/projection/validation module
- thin `patch-transaction status/project/validate` CLI dispatch
- deterministic no-apply example projection
- deterministic reports
- focused tests
- queue task packet
- evidence
- next-task prompt

Boundary:

- The capability target is `minimal_patch_transaction_schema`.
- It is representation, projection, validation, inspection, and reporting only.
- It must not approve, apply, mutate, roll back, admit, trust, execute workers,
  run providers, create branches/worktrees, call network services, publish, or
  promote anything.

Stop at `needs_review` and recommend exactly
`AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01` next.
