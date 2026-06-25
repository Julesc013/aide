# Migration Model

- current_schema_version: 1
- migrations are deterministic and idempotent
- rerunning migration v1 is accepted
- observed future migration versions are refused with `future_migration`
- destructive migrations are not implemented
