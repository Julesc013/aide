# Source Check Findings

The independent check recorded one material finding:

```text
capability_label.overclaims_observed_boundary
```

Observed prior active label:

```text
live_dominium_validation_command_readonly_v0
```

The label could be read as successful live validation or universal read-only
behavior. The observed proof is narrower: one registered command-boundary
invocation returned a typed Dominium refusal and no mutation was observed
within the declared probe coverage.

The source check also warned that AIDE booleans treated parsed Dominium JSON as
too broad a boundary proof for generic reuse. This relabel changes active
boundary fields so service-adapter entry and aggregate-validation execution are
not inferred from parseable JSON alone.
