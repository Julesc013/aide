# Final Decision

Decision: `ACCEPTED_WITH_WARNINGS`

Rationale:

- Required tests passed.
- Required validation passed.
- Required negative CLI checks fail closed.
- Canonical generated plan, target fixture, and expected fixture stayed
  unchanged.
- Temp workspace postimage matches expected postimage.
- Manual content is preserved.
- Rollback-compatible record exists.
- Rollback execution is not implemented or invoked.
- Reports parse and match observed files.
- Capability label and negative capability labels are truthful.
- No secrets were found.
- Forbidden operations were preserved.

Warnings are non-blocking and reflect deliberate scope limits:

- The accepted capability is only `fixture_temp_apply_only`.
- Formal public contract-envelope extraction remains future work.
- Broader conformance fixtures remain future work.
