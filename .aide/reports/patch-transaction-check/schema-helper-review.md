# Schema And Helper Review

Status: `PASS_WITH_WARNINGS`

The schema parses and the helper-produced transaction uses the expected
`apiVersion`, `kind`, `metadata`, `spec`, and `status` envelope shape.

The check reviewed helper/schema alignment for:

- transaction identity and provenance;
- repository/base/target representation;
- patch artifact representation;
- allowed, forbidden, and declared path scope;
- requirement references;
- lifecycle vocabulary;
- explicit execution facts;
- rollback-compatible and event references;
- explicit non-capabilities.

Warnings retained:

- Validation is a minimal structural and semantic subset, not a full JSON
  Schema Draft implementation.
- General diff parsing and artifact resolution are intentionally absent.
- Policy evaluation, approval, admission, trust, apply, rollback execution,
  event store, and runtime behavior are intentionally absent.

The material failures are in path-scope helper behavior, recorded separately.
