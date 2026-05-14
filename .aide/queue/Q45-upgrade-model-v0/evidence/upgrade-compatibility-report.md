# Upgrade Compatibility Report

Q45 compares the current AIDE install against the current `aide-lite-pack-v0` export pack without assuming SemVer where none exists. Compatibility is classified from pack metadata, policy/schema versions, command surfaces, file hashes, generated-state exclusions, and preservation rules.

## Compatibility Dimensions

- pack schema version
- policy schema version
- script command surface
- golden task catalog
- managed section format
- generated artifact format
- install plan schema
- repair plan schema
- refactor schema
- target-specific extension
- unknown

## Latest Comparison

- current installed files observed: 1784
- target-specific files observed: 861
- generated target-state files observed: 657
- portable source-pack files observed: 515
- differences classified: 515
- changed portable files: 1
- preserved target files: 861
- skipped source-state files: 8
- conflicts: 209
- required migrations: 8
- unsupported compatibility entries: 8
- unknown compatibility entries: 0

## Interpretation

The eight unsupported entries are source-state leak blockers in the current source pack comparison. They are not applied or migrated in Q45. The upgrade plan treats them as mandatory future migration candidates because source-generated state must not be copied as target truth.

## No-Apply Findings

- no upgrade apply operation exists.
- no overwrite/delete operation is allowed.
- target-specific state is preserved.
- generated source state is skipped or marked for future target-local regeneration/review.
