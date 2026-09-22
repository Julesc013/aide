---
type: AIDE Engineering Specification
title: Integration stage effects and observed closeout
status: adopted
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: adopted
  behavioral_qualification: source_tests_required
  owner: core/runtime/integration_broker
  source_aliases:
    - UR-INT-06
    - UR-INT-07
---

# Integration Stage Effects And Observed Closeout

## Scope

This bounded contract adopts only the per-stage effect and observed-closeout
behavior needed by the existing integration broker. It does not adopt the rest
of the imported integration-broker draft or qualify a provider, credential,
protected host, protected store, target policy, or server-side atomic predicate.

## Requirements

### AIDE-INT-001 - Exact Observation-Bound Stage Effects

Source alias: `UR-INT-06`.

Each consequential provider stage MUST have a distinct durable intent. A
mutation dispatcher MUST receive the exact canonical provider observation that
selected that stage and MUST revalidate its request, operation, intent, and
observation digest before child creation and while the child remains active.
Missing, stale, altered, or wrong-stage observations MUST refuse without a new
provider effect.

### AIDE-INT-002 - Observed Integration Closeout

Source alias: `UR-INT-07`.

A submitted or acknowledged provider mutation MUST NOT close the WorkUnit.
Closeout requires a later authoritative observation bound to the request,
candidate, required checks, merge result, and applicable target postconditions.
An uncertain acknowledgement MUST retain its intent and MUST NOT grant replay.

## Executable Acceptance

| Case | Requirement | Executable owner | Required result |
|---|---|---|---|
| `AIDE-INT-AC-001` | `AIDE-INT-001` | `test_continuous_worker_provider_bridge.py` | The child input contains the exact intent-bound observation and digest. |
| `AIDE-INT-AC-002` | `AIDE-INT-001` | `test_continuous_worker_provider_bridge.py` | Missing or altered observation binding refuses before child execution. |
| `AIDE-INT-AC-003` | `AIDE-INT-002` | `test_continuous_worker_pr_observation.py` and `test_continuous_worker_provider_bridge.py` | Submitted acknowledgement remains pending; only later integrated observation closes. |

The imported `UC-INT-06` and `UC-INT-07` designs remain source-level review
inputs. These executable AIDE cases are narrower and do not relabel those
unrun designs as passing tests.

## Qualification Boundary

Passing source and fixture tests establishes only the internal observation-to-
dispatch contract. Operational qualification still requires an actual protected
host and credential source, a fixed provider implementation, target-side stale
safety, hosted adversarial acceptance, and exact result observation.
