# Pagination Repair Acceptance

The repaired pagination behavior is accepted.

Facts:

- absent cursor fields are omitted;
- absent next page fields are omitted;
- no `cursor: null` appears;
- no `nextCursor: null` appears;
- present cursor values must be strings;
- invalid cursor values fail validation as material errors.

This closes the first material finding from the original failed check.
