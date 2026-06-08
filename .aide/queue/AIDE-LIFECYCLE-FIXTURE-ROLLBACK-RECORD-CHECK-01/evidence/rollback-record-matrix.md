# Rollback Record Matrix Evidence

Result: `PASS_WITH_WARNINGS`

Independent consistency check output:

```text
PASS rollback record independent consistency check
records=3 fixture_records=2 plans=13 expected_reports=7 linked_records=2
```

Fixture rollback records:

- `fixture-rollback-install-managed-section`: install phase, `fixture-plan-install-managed-section`, target class `fixture`, ownership `managed-section`, operation `update_managed_section`, hash checks PASS, inverse operation PASS, preconditions/stop conditions PASS, manual preservation PASS, protected path PASS, execution flags PASS.
- `fixture-rollback-upgrade-v2`: upgrade phase, `fixture-plan-upgrade-v2`, target class `fixture`, ownership `generated-file`, operation `update_managed_section`, hash checks PASS, inverse operation PASS, preconditions/stop conditions PASS, manual preservation PASS, protected path PASS, execution flags PASS.

Residual risk: static records are compatibility examples and remain review-gated.
