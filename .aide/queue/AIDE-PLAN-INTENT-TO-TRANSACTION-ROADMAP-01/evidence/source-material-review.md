# Source Material Review

The 2026-06-19 through 2026-06-20 architecture synthesis strengthens the plan
without replacing live queue truth.

Adopted planning points:

- AIDE is a portable intent-to-transaction control plane.
- AIDE should separate host axis from domain axis.
- Host Contract alone is not enough; Capability, Transaction, and
  Artifact/Event/Evidence contracts are also needed.
- `CapabilityInvocation` should become a first-class future object.
- PatchTransaction v1 should stay file-oriented and no-apply.
- Heterogeneous mutation should use a future DevelopmentTransaction envelope
  plus domain-owned mutation bundles.
- PreviewSession and ShadowWorkspace are key primitives before Workbench
  mutation.
- Dominium needs an integration charter and bridge conformance before broad
  Workbench implementation.
- First integration should prove validation and refusal/evidence mapping before
  scene mutation.

Not adopted as immediate implementation:

- Host Contract implementation.
- Workbench runtime or GUI.
- Scene edit preview/apply.
- Provider/model/network execution.
- Target repository apply.
