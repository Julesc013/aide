# ReferenceID Integration Review

Result: `PASS_WITH_WARNINGS`.

The OKF validation report records `aide_refs_parse: true`.

The generated pages use `aide://` references for schemas, capabilities, policies, artifacts, decisions, reports, events, and queue tasks. The structural validator routes these references through the ReferenceID helper.

`reference-id validate` remains `PASS_WITH_WARNINGS` in this check context.

No runtime reference registry, resolver service, database state, or provider-backed lookup was introduced.
