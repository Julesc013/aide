# Q08 Review Risks

## Must-Fix-Before-Post-Q08-Review

None.

Q08 is safe for post-Q08 foundation review. The review should rerun current commands rather than treating the stored `.aide/runs/self-check/latest.md` report as live canonical state.

## Should-Fix-Before-Next-Horizon

- `.aide/generated/manifest.yaml` remains stale by source fingerprint. Fix through a reviewed generated-artifact refresh/QFIX, not silently during review or automation.
- `.aide/commands/catalog.yaml` does not list `aide self-check`. Add this in a bounded metadata sync task before relying on command catalogs as a complete command-surface source.
- Q00-Q03, Q05, and Q06 raw status nuance remains visible. Reconcile or document these statuses in the post-Q08 foundation review before the next major horizon.
- The stored `.aide/runs/self-check/latest.md` report is an implementation evidence snapshot. After Q08 is marked passed, fresh `aide self-check` output should be used for current state.
- Live `aide self-check` still includes a static proposed follow-up line about Q08 review even after Q08 is marked passed, although the queue health and `next_recommended_step` are correct. Clean this up before self-check output becomes a stronger automation input.
- `aide-queue-next` and `aide-queue-run` report older raw review-gated items after Q08 passes because Q00-Q03/Q05/Q06 status nuance remains unresolved. This is visible and non-mutating, but should be reconciled before stronger automation depends on those helpers.

## Acceptable-Deferred

- Full YAML/JSON schema validation remains deferred.
- Automatic task packet generation remains deferred.
- Runtime, Service, Commander, external worker invocation, external CI, provider/model/network integration, release automation, and auto-merge remain deferred.
- Mutating Compatibility migrations remain deferred.
- Dominium-side adoption and real Dominium generated outputs remain deferred.
