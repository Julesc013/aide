# Dominium Bridge

## Purpose

Dominium Bridge is the first AIDE Bridge baseline. It records how Dominium can later consume AIDE as a pinned portable repo layer under XStack strict governance.

The bridge is AIDE-side metadata and policy. It is not Dominium product implementation, not a Runtime, not a provider adapter, and not a host.

## Implemented In Q07

Q07 adds:

- bridge metadata in `bridge.yaml`;
- adoption and validation guidance;
- XStack scope and portable mapping records;
- a Dominium/XStack profile overlay;
- stricter policy overlays;
- generated target expectation metadata;
- compatibility and pinning records.

## Boundary

Q07 does not modify any Dominium repository and does not emit real Dominium generated outputs.

XStack remains Dominium-local and strict. AIDE remains portable below it.

See [docs/reference/dominium-bridge.md](../../docs/reference/dominium-bridge.md) for the reference model.
