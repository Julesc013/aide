# Q07 Review Risks

Date: 2026-04-30
Reviewer: GPT-5.5 Codex

## Must Fix Before Q08

None identified for Q08 planning.

Q07 is sufficient for Q08 planning because the bridge baseline exists, Harness checks it structurally, XStack remains Dominium-local, generated target expectations are metadata-only, compatibility/pinning references Q06, and no hard validation errors were found.

## Should Fix Before Post-Q08 Automation

- Refresh `.aide/generated/manifest.yaml` with a reviewed generated-artifact refresh before automation depends on generated summaries or generated manifest currency.
- Decide how queue review outcomes should be represented without repeatedly staling Q05 generated artifacts.
- Refresh generated summaries in `AGENTS.md` and `.agents/skills/**` after approved source-input changes.
- Normalize stale high-level wording in `.aide/profile.yaml`, `.aide/components/catalog.yaml`, `.aide/policies/generated-artifacts.yaml`, and related summaries where they still describe already implemented Harness/Compatibility/Bridge work as planned or skeleton-only.
- Update `aide doctor` next-step guidance so it no longer says Q07 review is next after Q07 has passed.
- Teach queue helpers or future automation about review-gate/dependency posture before any autonomous worker uses `aide-queue-next` as an execution signal.

## Acceptable Deferred

- Full YAML or JSON Schema validation for bridge records.
- Dominium-side adoption, pin placement, and repository mutation.
- Real Dominium generated outputs.
- XStack proof execution.
- Bridge-pack or release-bundle packaging.
- Runtime, Hosts, Commander, Mobile, IDE extensions, provider/model/browser integrations, app surfaces, release automation, and autonomous service logic.
- Stronger policy comparison beyond explicit `stricter-than-aide` and `weakens_aide_policy: false` anchors.

## Residual Review Notes

The stale Q05 generated manifest source fingerprint is expected after Q07 implementation and this review status update. It is visible through `aide validate` as `GENERATED-SOURCE-STALE` and through `aide compile --dry-run` as `would_replace`.

This is not a blocker for Q08 planning, but Q08 should explicitly plan whether a generated-artifact refresh QFIX is required before self-hosting automation trusts generated summaries.
