# Source/Target Boundary

The AIDE source repository is not the installed target fixture.

The fixture uses:

```text
aide://fixture-target/aide-self-consumer-v0
```

as the synthetic installed target identity.

The fixture records `source_repo_is_target: false`, refuses source/target confusion, excludes source repo identity from target profile generation, and treats source-generated reports as source evidence rather than target truth.
