# Intent-To-Transaction Roadmap Plan

## Product Model

AIDE should remain the portable intent-to-transaction control plane. It
coordinates, governs, routes, records, and proves. It does not own every
domain's product semantics.

For Dominium, the intended separation is:

- AIDE coordinates and proves.
- Dominium defines product law.
- Domino performs admitted deterministic capabilities.
- Workbench captures intent and makes plans, previews, evidence, and recovery
  legible.
- Dominium Bridge maps meanings between AIDE and Dominium without copying one
  repo's concepts into the other.

## Roadmap Decision

The accepted ContextPack v2 resume task recommends
`AIDE-BUILD-INTEROP-EXPORTS-01`, and this plan preserves that serialized next
task. Static interop exports are still safe as the next AIDE-local step because
they are deterministic, report-only previews.

After that static interop step, the next architectural lane should focus on the
cross-repo seam and contract families before broad Workbench or runtime work:

1. `AIDE-DOMINIUM-INTEGRATION-CHARTER-01`
2. `AIDE-BUILD-CAPABILITY-INVOCATION-CONTRACT-01`
3. `AIDE-CHECK-CAPABILITY-INVOCATION-CONTRACT-01`
4. `AIDE-ACCEPT-CAPABILITY-INVOCATION-CONTRACT-01`
5. `AIDE-BUILD-HOST-CONTRACT-V0-01`
6. `AIDE-CHECK-HOST-CONTRACT-V0-01`
7. `AIDE-ACCEPT-HOST-CONTRACT-V0-01`
8. `AIDE-BUILD-DOMINIUM-BRIDGE-MANIFEST-01`
9. `AIDE-BUILD-DOMINIUM-BRIDGE-CONFORMANCE-01`
10. `AIDE-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`
11. `AIDE-BUILD-DEVELOPMENT-TRANSACTION-CONTRACT-01`
12. `AIDE-BUILD-PREVIEW-SESSION-CONTRACT-01`
13. `AIDE-BUILD-WORKBENCH-READONLY-01`

## Design Rule

Do not build a contract cathedral. Each new abstraction should be justified by
a narrow vertical slice, starting with validation and read-only projections
before document preview, scene preview, apply, graph, asset, build, simulation,
performance, or legacy-host workflows.
