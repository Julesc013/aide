# Dominium Bridge Validation

## Q07 Validation Boundary

Q07 validation is structural and AIDE-side only.

Harness v0 checks required bridge files and simple anchors. It does not parse full YAML, run Dominium proofs, mutate the Dominium repo, call providers, call models, access the network, or generate real Dominium outputs.

## Required Records

- `bridges/dominium/bridge.yaml`
- `bridges/dominium/adoption.md`
- `bridges/dominium/validation.md`
- `bridges/dominium/compatibility.yaml`
- `bridges/dominium/xstack/scope.md`
- `bridges/dominium/xstack/portable-mapping.yaml`
- `bridges/dominium/profiles/dominium-xstack.profile.yaml`
- `bridges/dominium/policies/review-gates.yaml`
- `bridges/dominium/policies/proof-gates.yaml`
- `bridges/dominium/policies/generated-artifacts.yaml`
- `bridges/dominium/generators/targets.yaml`
- `docs/reference/dominium-bridge.md`

## Anchor Checks

Q07 structural validation expects these facts:

- bridge baseline id is `aide.dominium-bridge.v0`;
- XStack is `Dominium-local` and strict;
- policy overlays declare `base_policy_relation: stricter-than-aide`;
- generated target metadata declares `emits_outputs: false`;
- compatibility records reference `aide.compat-baseline.v0`;
- external Dominium repository mutation is prohibited.

## Failure Handling

Missing required bridge files are hard structural errors.

Missing strictness, pinning, or no-output anchors are hard structural errors because they could weaken the bridge boundary.

Generated manifest drift caused by Q07 source-input changes is expected to remain a warning unless a later task explicitly authorizes deterministic refresh.
