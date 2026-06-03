# Implementation Summary

`AIDE-APPLY-02 - Scoped Transaction Executor v0` is implemented and review-gated.

## Executor Entry Point

- Core module: `core/apply/transaction_executor.py`
- Public APIs: `load_transaction_plan`, `execute_plan_file`, `execute_transaction_plan`, and `compute_text_hash`
- AIDE Lite command family: `py -3 .aide/scripts/aide_lite.py scoped-transaction <status|validate|fixture-plan|fixture-verify|run --plan>`

## Transaction Plan Format

The executor accepts explicit JSON plans with schema version `aide.scoped-transaction-plan.v0`. Required fields include transaction id, mode, allowed roots or paths, protected roots, operation allowlist, report path, rollback record path, and an explicit operation list.

Supported modes are `dry-run`, `report`, and explicit `apply`. Dry-run/report mode writes evidence and does not mutate target files. Apply mode is explicit and executes only after the same safety checks pass.

## Allowed Operation Types

- `update_managed_section`
- `report`
- `validate`
- `noop`

Missing, ambiguous, unsupported, install apply, upgrade apply, repair apply, rollback/uninstall apply, target mutation, branch/worktree mutation, provider/model/Gateway/network, release/publication, broad active-repo apply, broad delete, and broad move operation types are rejected.

## Safety Behavior

- Paths are normalized as repo-relative paths.
- Absolute paths, path traversal, wildcard or bulk expansion, protected paths, and paths outside explicit allowed roots or paths are blocked.
- Managed-section updates reuse `core.apply.managed_sections`.
- Missing, duplicate, malformed, nested, unsupported, or ambiguous managed-section marker ownership states block execution.
- Preimage hash checks are required before mutation-capable operations.
- Postimage verification is performed against expected postimage content or hash where provided.
- Staged-change and rollback-compatible records are written.
- Failures produce blocker records and fail closed.

## Capability Reality

The implemented capability is `implemented`, `tested`, `fixture-tested`, `report-backed`, and `review-gated`.

It is not production-ready, release-ready, install-capable, upgrade-capable, repair-capable, rollback/uninstall-capable, target-repo-capable, provider/model capable, Gateway capable, network capable, or broad active-repo apply capable.
