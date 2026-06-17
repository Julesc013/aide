# ReferenceID Integration Review

Result: `ACCEPTED_WITH_WARNINGS`.

Accepted ReferenceID integration:

- OKF validation reports `aide_refs_parse: true`
- generated pages use stable `aide://` identifiers for schemas, capabilities, policies, artifacts, decisions, reports, events, and queue tasks
- ReferenceID predecessor validation remains `PASS_WITH_WARNINGS`

The acceptance does not add a runtime reference registry, resolver service, database state, provider-backed lookup, or target mutation.
