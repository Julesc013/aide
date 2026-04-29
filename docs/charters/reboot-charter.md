# AIDE Reboot Charter

## Goal

The AIDE reboot refactors the existing repository in place so future work can proceed from a smaller, clearer self-hosting model. The reboot should make AIDE able to prompt, queue, validate, and improve itself through filesystem-based ExecPlans while preserving the bootstrap-era history and evidence already in the repository.

## Public Model

- AIDE Core: shared contracts, harnesses, compatibility logic, runtime-facing boundaries, control policy, and SDK-facing extension points.
- AIDE Hosts: IDE or tool-host integrations and host-family proof lanes, including modern and historical environments.
- AIDE Bridges: bounded connection layers that let Core capabilities operate through local proof profiles, host adapters, generated artifacts, or companion surfaces.

## Internal Core Split

- Contract: stable profiles, schemas, request and response shapes, capability declarations, and architecture constraints.
- Harness: deterministic validation, fixtures, queue checks, evidence capture, and repeatable proof execution.
- Runtime: future execution substrate for richer behavior. Q00 does not build it.
- Compatibility: host, platform, version, migration, and support posture records that keep claims honest.
- Control: queue policy, review gates, autonomy boundaries, governance links, and operating records.
- SDK: future extension-facing surfaces for authored integrations. Q00 does not build it.

## First Shipped Stack

The first shipped reboot stack is:

- Contract
- Harness
- Compatibility
- Dominium Bridge

Dominium Bridge is the first bridge target for the reboot. XStack remains Dominium's strict local governance and proof profile. This charter records the target stack; it does not claim the stack is implemented.

## Non-Goals

- No immediate full Runtime.
- No immediate Commander.
- No immediate Mobile.
- No immediate IDE extension family.
- No Visual Studio, Xcode, VS Code, or other host implementation in Q00.
- No provider or model integration in Q00.
- No destructive repository rewrite.
- No deletion or rewrite of bootstrap-era phase history.
- No release, publishing, tagging, packaging automation, or merge-to-main action.

## Operating Constraints

- `.aide/queue/` is canonical for non-trivial self-hosting work.
- ExecPlans are the durable unit of long-running autonomous work.
- Generated outputs must be deterministic and reviewable.
- Queue items must stop at blockers and review gates.
- Future implementation claims must be backed by repository evidence.
