# Q04 Review Risks

Date: 2026-04-30

## Must Fix Before Q05

No must-fix issues block Q05 planning.

Q05 implementation must still wait for its own plan, generated-artifact policy details, drift checks, validation evidence, and review gate. Passing Q04 does not authorize Q05 implementation.

## Should Fix Before Q06

- Refresh Q03-era contract wording in `.aide/profile.yaml`, `.aide/toolchain.lock`, and `.aide/commands/catalog.yaml` so canonical contract records describe Harness v0 as implemented rather than planned/not implemented.
- Decide whether Q00 through Q03 should be moved from `needs_review` to an accepted review state based on the existing foundation review, or whether separate lightweight review/status cleanup is required.
- Improve queue helper semantics in a future queue automation task so `scripts/aide-queue-next` can account for review gates and dependency posture, not only raw pending status.
- Harden structural validation into stronger schema validation only after a reviewed decision on parser/schema strategy.

## Acceptable Deferred

- Full YAML or JSON Schema validation is deferred.
- Generated downstream artifacts, generated-file markers, and stale-output drift detection remain Q05.
- Compatibility baseline and migration hardening remain Q06.
- Dominium Bridge baseline remains Q07.
- Runtime, Service, Hosts, Commander, Mobile, IDE extensions, providers, app surfaces, packaging, release automation, and autonomous worker execution remain later work.

## Review Notes

The stale Q03 contract wording is visible and warned on by Harness v0. It does not make Q05 planning unsafe because generated artifact planning can depend on the actual command behavior and can require a contract refresh before generation if needed.

The status-only queue-next behavior is safe for manual Q05 planning, but it is not safe enough for autonomous execution. Q08 or a narrower queue-helper task should address that before automation grows teeth.
