# Recommended Next Work

Because the check found a material profile digest defect, the next task is:

```text
AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
```

Repair should be bounded to:

- profile digest source semantics;
- validation failure on raw-profile digest mismatch;
- focused tests for independent raw-profile digest recomputation;
- regenerated ConformanceResult reports and evidence.

Do not proceed to ConformanceResult acceptance until the repair is built and
checked.
