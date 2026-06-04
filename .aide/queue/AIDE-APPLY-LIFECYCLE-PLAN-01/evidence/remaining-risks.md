# Remaining Risks

- `AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01` is selected but not created or executed in this task.
- Task OS `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01` because Task OS selector logic has not been extended to consume this lifecycle plan's `next-batch.md`. This task did not change implementation files.
- PyYAML is unavailable in the current Python environment, so YAML validation relies on repo parsing and structural checks.
- Broad changed-file secret scans may find existing policy/test marker strings in `aide_lite.py`; diff-added-line scan is required to distinguish new credential risk.
- Fixture lifecycle schemas are not yet defined.
- Rollback records are evidence contracts only until a future rollback task explicitly authorizes execution.
- Active AIDE repo apply, target repo adoption, release/promotion, provider/model, Gateway, and network surfaces remain blocked or deferred.
- Token quality ledger evidence is not yet sufficient for strong token/cost-saving or quality-improvement claims.
