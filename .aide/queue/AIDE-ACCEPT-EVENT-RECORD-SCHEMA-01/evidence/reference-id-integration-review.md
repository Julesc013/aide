# ReferenceID Integration Review

## Result

PASS

## Accepted

- `event_ref` uses `aide://event/<id>`.
- `subject.ref` uses `aide://...`.
- `causation.ref` and `correlation.ref` use `aide://...` when present.
- Evidence refs use `aide://evidence/...`.
- Report refs use `aide://report/...`.
- Actor refs use `aide://...` where represented as refs.
- File paths remain locators, not identity.
- EventRecord does not create a new reference grammar.
- `reference-id validate` still passes with warnings limited to its own projection-only boundary.
