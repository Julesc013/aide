# AIDE Reboot Doctrine

## Status

Current status: partial. Q01 defines the documentation doctrine. Later queue items must provide structural, contract, harness, compatibility, and bridge evidence before claiming implementation.

## Doctrine

AIDE is an existing bootstrap-era repository being refactored in place. The reboot keeps historical records intact and narrows future work into reviewable filesystem queue items.

The canonical public model is:

- AIDE Core: durable semantics, contracts, harnesses, compatibility records, control policy, runtime boundaries, and SDK-facing extension points.
- AIDE Hosts: IDE or tool-host shells, host-family proof lanes, and host-specific adapters.
- AIDE Bridges: bounded connection layers between AIDE Core semantics and local proof profiles, host adapters, generated artifacts, or companion surfaces.

The internal AIDE Core split is:

- Contract: profiles, schemas, capabilities, request and response shapes, and architecture constraints.
- Harness: deterministic validation, fixtures, queue checks, evidence capture, and proof execution.
- Runtime: future execution substrate. It is deferred by Q01.
- Compatibility: host, platform, version, migration, support, and capability posture.
- Control: queue policy, review gates, autonomy boundaries, governance links, and execution records.
- SDK: future authored integration surfaces. It is deferred by Q01.

The first shipped reboot stack is Contract + Harness + Compatibility + Dominium Bridge. Dominium Bridge is the first bridge target. XStack is Dominium's strict local governance and proof profile, not a generic AIDE product layer.

## Autonomy Rule

"Do everything until done" becomes queue-driven autonomy. Non-trivial work must be represented by an AIDE queue item, an ExecPlan, bounded allowed paths, evidence, validation, and review gates. Small direct work is allowed only under the bypass policy.

## Reality Boundary

The repo is pre-product. Existing bootstrap-era implementation and proof records are real, but Q01 does not make Runtime, Commander, Mobile, IDE Hosts, provider adapters, app surfaces, release automation, or packaging automation complete.
