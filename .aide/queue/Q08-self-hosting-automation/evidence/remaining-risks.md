# Q08 Remaining Risks

## Must Fix Before Post-Q08 Automation

- Q08 needs independent review before any post-Q08 foundation review or broader automation planning.
- Automation consumers must not treat `aide doctor`, `aide self-check`, or queue helper output as permission to mutate the repo.

## Should Fix Before Broader Automation

- `.aide/generated/manifest.yaml` remains stale by source fingerprint. It should be refreshed only by a reviewed generated-artifact QFIX.
- `.aide/commands/catalog.yaml` does not yet list `aide self-check`. Q08 did not edit the command catalog because it was outside the implementation allowed paths; a reviewed metadata-sync task should decide whether to update it.
- Q00-Q03 remain raw `needs_review` without item-local review outcomes. Foundation review evidence accepted proceeding, but future automation would benefit from a reconciled status model.
- Q05 and Q06 remain raw `needs_review` despite `PASS_WITH_NOTES` review evidence. Q08 reports this nuance rather than rewriting history.

## Acceptable Deferred

- Full YAML/schema validation remains deferred.
- Mutating Compatibility migrations remain deferred.
- Proposed queue task generation remains deferred.
- Runtime, Service, Commander, Hosts, Mobile, provider/model integrations, browser bridges, app surfaces, external CI, release automation, auto-merge, and external worker invocation remain deferred.
- Dominium-side adoption and real Dominium generated outputs remain deferred.
