# Q06 Remaining Risks

Date: 2026-04-30

## Must Fix Before Q06 Review

None identified.

Q06 is intentionally stopped at `needs_review` and requires an independent review before Q07 planning.

## Should Fix Before Q07

- `.aide/profile.yaml` still contains Q05-era current-focus wording because Q06 was not allowed to modify it. Compatibility truth now lives in `.aide/compat/**`, `.aide/toolchain.lock`, docs, and Q06 evidence.
- `.aide/policies/generated-artifacts.yaml` still contains Q03-era planned-boundary wording. This was already recorded by Q05 review as a cleanup before Q07 or broader generated-output work.
- Generated sections in `AGENTS.md` and `.agents/skills/**` still contain Q05-era concise deferral wording because Q06 did not alter generated-artifact generator bodies or target policy.
- Q00 through Q03 and Q05 still have raw `needs_review` queue statuses; Q05 review evidence records `PASS_WITH_NOTES` and explicitly permitted Q06.

## Acceptable Deferred

- Full YAML or JSON Schema validation.
- Mutating migrations and migration apply mode.
- Compatibility shims.
- Runtime replay.
- Dominium Bridge baseline and XStack bridge implementation.
- Runtime, Hosts, Commander, Mobile, IDE extensions, provider/model integrations, browser bridges, app surfaces, release automation, and autonomous service logic.

## Scope Risks Avoided

- No real migration platform was built.
- No generated artifact behavior was changed.
- No final Claude targets or unsafe hooks were created.
- No Runtime, Host, provider, app, release, or Dominium Bridge implementation was added.
