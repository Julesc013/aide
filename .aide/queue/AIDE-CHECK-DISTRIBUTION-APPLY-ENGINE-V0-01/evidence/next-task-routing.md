# Next Task Routing

Recommended next task:

`AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-REPAIR-01`

Repair scope should be bounded to:

- require `update_plan_ref` before execution
- require `rollback_bundle_ref` before execution
- validate source distribution, project lock, and ownership ledger refs against accepted fixture context
- refuse execution when accepted context is missing
- add focused regression tests for these fail-closed cases
- regenerate affected reports and evidence

Do not accept DistributionApplyEngine v0 until a repair check passes with `material_finding_count: 0` and `missing_evidence: 0`.
