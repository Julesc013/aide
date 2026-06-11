# Scenario Review

Scenario: `install-managed-section`

Fixture root:

- `.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section`

Target file:

- `manual/with-managed-section.md`

Operation:

- `update_managed_section`

The target and expected files have managed-section markers. The operation is expected to replace only the managed section and preserve manual content outside markers.
