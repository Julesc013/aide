# Q07 Remaining Risks

Date: 2026-04-30

## Must Fix Before Q08

- Q07 needs independent review before Q08 self-hosting automation or any Dominium-side adoption work.
- `.aide/generated/manifest.yaml` is stale by source fingerprint because Q07 changed generated-artifact source inputs. This should be refreshed only by a reviewed task that is allowed to run deterministic generated artifact refresh.

## Should Fix Soon

- `.aide/profile.yaml` still contains Q05/Q06-era high-level wording such as `compatibility_baseline: not_implemented` and `dominium_bridge: skeleton_only`. Q07 could not update it because `.aide/profile.yaml` was not in the Q07 allowlist.
- `.aide/policies/generated-artifacts.yaml` still contains Q03-era planned-boundary wording. This was noted by Q05/Q06 reviews and remains cleanup for a later reviewed task.
- Generated summaries in `AGENTS.md` and `.agents/skills/**` remain stale until generated artifacts are refreshed.
- Queue status cleanup for Q00-Q03, Q05, and Q06 remains unresolved because review tasks avoided index changes to prevent hidden generated-manifest drift.

## Acceptable Deferred

- Full YAML/schema validation for bridge records.
- Dominium-side adoption and pin placement.
- Real Dominium generated outputs.
- XStack proof execution.
- Bridge-pack or release-bundle packaging.
- Runtime, Hosts, Commander, Mobile, IDE extensions, provider/model/browser integrations, app surfaces, release automation, and autonomous service logic.

## Non-Blockers For Q07 Review

- `aide validate` has no hard errors.
- Dominium Bridge files and required anchors are present.
- Generated manifest stale-source warning is expected and review-visible.
- No external Dominium repository path was modified.
