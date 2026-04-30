# Post-Q08 Foundation Review

## Executive Verdict

The initial AIDE reboot foundation from Q00 through Q08 is complete enough to close Horizon 1 and begin the next horizon of planning, provided the next horizon starts with a small cleanup track before new feature work.

The foundation now has:

- declarative Profile/Contract truth under `.aide/`;
- executable local Harness checks and reports;
- deterministic generated-artifact markers, manifest, preview, and drift detection;
- a conservative Compatibility baseline with no-op migration posture;
- an AIDE-side Dominium Bridge baseline with XStack kept Dominium-local;
- report-first self-hosting automation that does not invoke external agents or mutate canonical truth by default.

The remaining issues are warning-level cleanup, not foundation blockers. They are visible in Harness output and review evidence.

## Current Commit / Branch / Worktree State

Observed at review start:

- Branch: `main`
- Tracking: `origin/main`
- Latest commit: `15d9fd7 Review Q08 self-hosting automation`
- Worktree: clean before this review packet was created

This review intentionally did not modify implementation, Contract, generated artifact, Compatibility, Bridge, or self-check report files.

## Q00-Q08 Status Table

| Queue item | Raw queue status | Planning state | Review evidence | Foundation classification |
| --- | --- | --- | --- | --- |
| Q00-bootstrap-audit | `needs_review` | `active` | foundation/full-audit context only | Historical bootstrap record, cleanup needed |
| Q01-documentation-split | `needs_review` | `implemented` | later queue authorization and foundation context | Accepted for dependency by later evidence, cleanup needed |
| Q02-structural-skeleton | `needs_review` | `implemented` | later queue authorization and foundation context | Accepted for dependency by later evidence, cleanup needed |
| Q03-profile-contract-v0 | `needs_review` | `implemented` | later queue authorization and foundation context | Accepted for dependency by later evidence, cleanup needed |
| Q04-harness-v0 | `passed` | `implemented` | `PASS_WITH_NOTES` | Accepted |
| Q05-generated-artifacts-v0 | `needs_review` | `implemented` | `PASS_WITH_NOTES` | Accepted by review evidence, cleanup needed |
| Q06-compatibility-baseline | `needs_review` | `implemented` | `PASS_WITH_NOTES` | Accepted by review evidence, cleanup needed |
| Q07-dominium-bridge-baseline | `passed` | `implemented` | `PASS_WITH_NOTES` | Accepted |
| Q08-self-hosting-automation | `passed` | `implemented` | `PASS_WITH_NOTES` | Accepted |

The raw queue status mismatch for Q00-Q03, Q05, and Q06 is a queue hygiene issue. It is not hidden: `aide validate`, `aide self-check`, `aide-queue-next`, and `aide-queue-run --no-prompt` all expose it.

## Architecture Review

The public model remains AIDE Core, AIDE Hosts, and AIDE Bridges. The internal Core split remains Contract, Harness, Runtime, Compatibility, Control, and SDK.

The first shipped stack is now represented at the AIDE repo foundation level:

- Contract/Profile: Q03
- Harness: Q04
- generated artifacts: Q05
- Compatibility: Q06
- Dominium Bridge: Q07
- report-first self-hosting automation: Q08

Runtime, Hosts, Commander, Mobile, IDE extensions, provider adapters, browser bridges, app surfaces, release automation, Pack/Skill/Workflow IR, and external worker automation remain deferred.

## Source-Of-Truth Review

The source-of-truth boundaries remain intact:

- `.aide/` remains canonical for Profile/Contract records.
- `.aide/queue/` remains canonical for queue execution state.
- generated outputs remain non-canonical compiled or managed outputs.
- `.aide/generated/manifest.yaml` is a generated manifest, not canonical truth.
- `.aide/runs/self-check/latest.md` is non-canonical report evidence.
- bootstrap-era directories and records remain historical evidence and were not deleted.

No review action created a new canonical truth source.

## Contract/Profile Review

Q03 established the declarative Profile/Contract surface and source-of-truth docs. Current validation confirms the required `.aide/` directories, profile, toolchain lock, component catalog, command catalog, policies, tasks, evals, adapters, and compatibility records exist.

Known cleanup remains: old raw queue statuses and some root/candidate docs still carry review-gated nuance or stale forward pointers. That should be corrected through a bounded cleanup task rather than silently rewriting history inside this review.

## Harness Review

`scripts/aide` exists and exposes:

- `init`
- `import`
- `compile`
- `validate`
- `doctor`
- `migrate`
- `bakeoff`
- `self-check`

The Harness is local, deterministic, and standard-library oriented. Command smoke passed. `aide validate` and `aide doctor` returned `PASS_WITH_WARNINGS`, with warnings limited to older review-gate statuses and stale generated manifest source fingerprint.

`aide doctor` now points to the post-Q08 foundation review rather than the stale Q07 review guidance. This satisfies the Q08 carry-forward correction.

## Generated-Artifact Review

Q05 generated-artifact policy exists and the marker/manifest/drift model is active. `aide compile --dry-run` reported:

- `mutation: none`
- generated artifacts are non-canonical
- managed targets are current
- `.aide/generated/manifest.yaml` would be replaced because its source fingerprint is stale
- Dominium Bridge targets are metadata-only and emit no real outputs

The stale manifest source fingerprint is visible and expected after later queue/source changes. This review did not run `compile --write` and did not refresh generated artifacts.

No unsafe Claude hooks or autonomous bypass agents were found.

## Compatibility Review

Q06 Compatibility baseline exists under `.aide/compat/**` and `core/compat/**`. `aide migrate` reports:

- baseline version `aide.compat-baseline.v0`
- no-op current migration engine
- no mutating migrations
- unknown future versions are errors

Compatibility records cover known v0 surfaces for profile, toolchain, queue index/policy/status, command catalog, generated manifest, generator version, and Harness command surface. Replay remains structural and explicitly not Runtime replay.

## Dominium Bridge Review

Q07 Dominium Bridge baseline exists inside the AIDE repo under `bridges/dominium/**` and `docs/reference/dominium-bridge.md`.

The bridge remains AIDE-side only:

- XStack is Dominium-local and strict.
- Bridge records are downstream overlays, not generic AIDE Core doctrine.
- generated target records are metadata only.
- no external Dominium repository was touched.
- no real Dominium generated outputs were emitted.

Harness validation checks the bridge records and boundary anchors structurally.

## Self-Hosting Automation Review

Q08 added report-first local self-hosting automation. `aide self-check` reports:

- validation posture;
- queue health and review-gate nuance;
- generated artifact drift;
- Compatibility smoke posture;
- Dominium Bridge status;
- proposed follow-ups;
- next recommended step.

The command explicitly reports no external calls, no provider/model calls, no network calls, no automatic worker invocation, and no queue auto-merge.

`aide self-check --write-report` was not run during this review because writing `.aide/runs/self-check/latest.md` is outside the allowed paths for this post-Q08 review. The existing report was inspected and treated as non-canonical snapshot evidence.

## Queue Health Review

Queue helpers remain manual/report oriented:

- `aide-queue-status` prints all queue item raw statuses.
- `aide-queue-next` currently points at Q06 because Q06 raw status remains `needs_review`.
- `aide-queue-run --no-prompt` reports Q06 review-gate posture and review evidence nuance without invoking workers or mutating files.

This is conservative but noisy. The next horizon should include a queue/status reconciliation cleanup so helpers can reflect accepted review evidence without deleting historical records.

## Unresolved Warning Review

Known warnings:

- Q00-Q03 raw statuses remain `needs_review`.
- Q05 and Q06 raw statuses remain `needs_review` despite `PASS_WITH_NOTES` review evidence.
- `.aide/generated/manifest.yaml` source fingerprint is stale.
- `.aide/commands/catalog.yaml` does not yet list `aide self-check`.
- `aide self-check` live output still includes a stale proposed follow-up saying Q08 review is next, even though its next recommended step is correct.
- README, ROADMAP, and one PLANS summary line still contain stale Q08 review phrasing.
- `.aide/runs/self-check/latest.md` is a pre-review snapshot and not current live state.

None of these are hard blockers for next-horizon planning. They should be handled before substantive next-horizon feature work.

## Next-Horizon Readiness

The foundation is ready for the next horizon if the first next-horizon work is cleanup/reconciliation, not new feature implementation.

Recommended first cleanup sequence:

1. `QFIX-h1-status-catalog-doc-cleanup`
2. `QFIX-generated-artifact-refresh-v0`
3. `Q09-next-horizon-planning`

The cleanup should keep history intact, preserve review evidence, and avoid broad architecture changes.

## Final Decision Marker

FOUNDATION_COMPLETE_WITH_CLEANUP_NOTES
