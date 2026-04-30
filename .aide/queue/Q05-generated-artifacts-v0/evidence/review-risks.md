# Q05 Review Risks

## Must Fix Before Q06

None.

Q05 generated artifacts v0 is sufficient for Q06 planning. The remaining issues are cleanup or later hardening items, not blockers.

## Should Fix Before Q07

- `.aide/policies/generated-artifacts.yaml` still says generated artifacts are a Q03 planned boundary and not implemented. Q05 evidence explains why it was not edited, but the policy record should be normalized before the Dominium Bridge or broader generated-output work depends on it.
- Queue status finalization now interacts with Q05 manifest freshness because `.aide/queue/index.yaml` is a manifest source input. A future QFIX, Q06 planning task, or Q06 implementation preflight should either refresh the manifest after queue metadata changes or explicitly record the expected stale-source warning.
- Q00 through Q03 still have `needs_review` queue statuses. Foundation and Q04/Q05 reviews found them coherent enough to proceed, but the queue should eventually be cleaned up or explicitly superseded.

## Acceptable Deferred

- Full YAML/schema validation is still deferred. Q05 v0 uses structural text, marker, and fingerprint checks.
- Source-fingerprint drift is a warning/review-required condition rather than a hard error. This is acceptable for Q05 v0, but Q06 should decide whether Compatibility needs stricter severity.
- Final root `CLAUDE.md`, `.claude/settings.json`, and `.claude/agents/**` remain deferred. This is intentional and safer than emitting final Claude-specific targets in Q05.
- Broader generated skill families such as `aide-contract`, `aide-harness`, and `aide-generated-artifacts` remain deferred.
- The generated manifest parser is line-oriented and not a full YAML parser.

## Scope Risks Avoided

- No provider/model/network/browser code was introduced.
- No Runtime, Service, Host, Commander, Mobile, IDE extension, Compatibility baseline, or Dominium Bridge implementation was added.
- No final Claude targets or unsafe hooks were introduced.
