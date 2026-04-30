# Q06 Review Risks

Date: 2026-04-30
Reviewer: GPT-5.5 Codex

## Must Fix Before Q07

None identified.

Q06 is sufficient for Q07 planning because the Compatibility baseline records exist, `aide validate` checks them, `aide migrate` reports them non-destructively, and replay/upgrade/deprecation posture is explicit.

## Should Fix Before Q08

- Refresh `.aide/profile.yaml` current-focus and implemented-reality wording so it no longer says Q06 Compatibility baseline is planned or not implemented.
- Normalize `.aide/policies/generated-artifacts.yaml`, which still contains Q03-era planned-boundary wording for generated artifacts.
- Consider updating `.aide/policies/compatibility.yaml` wording so it distinguishes no-op migration records from a future migration engine more clearly.
- Refresh generated summaries in `AGENTS.md` and `.agents/skills/**` after any approved source-input update so they no longer imply Q06+ Compatibility work is deferred.
- Decide how to mark Q00-Q03 and Q05 review outcomes without creating hidden `.aide/generated/manifest.yaml` drift.

## Acceptable Deferred

- Full YAML or JSON Schema validation.
- Mutating migrations and migration apply mode.
- Compatibility shims.
- Runtime replay.
- Dominium Bridge implementation and XStack bridge proof behavior.
- Runtime, Hosts, Commander, Mobile, IDE extensions, provider/model integrations, browser bridges, app surfaces, release automation, and autonomous service logic.
- Queue helper dependency/review-gate awareness beyond status-only `aide-queue-next`.

## Residual Review Notes

Q06 intentionally preserves conservative boundaries. These deferred items are not blockers for Q07 planning, but Q07 should read `.aide/compat/**`, `docs/reference/compatibility-baseline.md`, and this review evidence rather than relying only on generated high-level summaries.
