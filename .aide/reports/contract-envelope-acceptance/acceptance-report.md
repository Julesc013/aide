# Contract Envelope Acceptance

Task: `AIDE-ACCEPT-CONTRACT-ENVELOPE-01`

Result: `ACCEPTED_WITH_WARNINGS`

## Summary

The minimal contract envelope slice is accepted as the current reusable
protocol foundation. The accepted capability is limited to the `aide.dev/v1alpha1`
envelope helper, `apiVersion/kind/metadata/spec/status`, minimal schema subset
runtime validation, helper/schema alignment, lifecycle fixture report
projections, `contract-envelope status/project/validate`, and
backward-compatible validation of accepted lifecycle fixture reports.

Schema runtime validation is real, helper/schema alignment is real, accepted
lifecycle reports remain compatible, projections are additive, unknown optional
fields are tolerated, unknown required capabilities fail closed, tests pass, and
validation passes.

## Warnings

- PyYAML is unavailable; stdlib structural YAML checks and repo validation passed.
- Full JSON Schema Draft 2020-12 validation remains deferred by design.
- Broad secret scan flagged existing test/policy marker strings in `aide_lite.py`;
  no secret value was found.

## Non-Capabilities

This acceptance does not accept full JSON Schema Draft 2020-12 support, full
public protocol stability, full kernel schema, EvidencePacket schema, WorkUnit
schema or CLI, TestJob schema, Test Broker, Service, Commander, provider
adapters, branch/worktree automation, target repo apply, active repo apply,
rollback execution, production readiness, release readiness, network, Gateway,
GitHub mutation, or model/provider calls.

## Next

Recommended next task: `AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01`.
