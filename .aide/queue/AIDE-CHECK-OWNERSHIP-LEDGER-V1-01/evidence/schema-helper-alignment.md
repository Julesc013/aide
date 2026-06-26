# Schema Helper Alignment

- JSON Schema parses and defines a Draft 2020-12 OwnershipLedger envelope.
- Helper output conforms to the live schema.
- Valid source fixtures pass and invalid source fixtures fail with stable source
  refusal codes.
- Optional extensions are represented by explicit `extensions` maps and
  tolerated when optional.
- Unknown required features and `requires.*` extensions fail closed.

Material gap: the schema/helper envelope is aligned with the current compact
implementation, but not with the richer file-entry and managed-section contract
required by this check.
