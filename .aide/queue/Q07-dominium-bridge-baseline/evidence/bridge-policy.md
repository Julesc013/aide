# Q07 Bridge Policy Evidence

Date: 2026-04-30

## Bridge Model

Q07 implements an AIDE-side Dominium Bridge baseline.

The bridge owns:

- bridge metadata;
- adoption guidance;
- validation expectations;
- XStack boundary records;
- Dominium/XStack profile overlay;
- strict policy overlays;
- generated target expectation metadata;
- compatibility and pinning records;
- structural Harness bridge checks.

The bridge does not own:

- Dominium product semantics;
- Dominium Runtime;
- XStack proof execution;
- external Dominium repository mutation;
- real Dominium generated outputs;
- generic AIDE Core semantics;
- provider/model/browser/network behavior;
- Runtime, Hosts, Commander, Mobile, IDE extension, app, release, or autonomous service behavior.

## XStack Boundary

XStack remains Dominium-local and strict.

Q07 records XStack as a Dominium governance and proof profile above portable AIDE. It does not promote XStack into generic AIDE doctrine and does not implement XStack internals.

## Policy Strictness

Policy overlays under `bridges/dominium/policies/**` declare:

- `base_policy_relation: stricter-than-aide`;
- `weakens_aide_policy: false`;
- generated outputs are deferred and non-canonical;
- unsafe hooks and autonomous bypass agents are prohibited;
- AIDE pin changes, bridge baseline changes, generated target writes, proof gate changes, and external Dominium repo mutation require review.

## Compatibility And Pinning

`bridges/dominium/compatibility.yaml` references:

- `aide.profile-contract.v0`;
- `aide.compat-baseline.v0`;
- `aide.generated-manifest.v0`;
- `q05.generated-artifacts.v0`;
- `aide.harness-command-surface.v0`.

It records `pinned-managed-repo-layer` as the recommended adoption mode and states that pin changes require review. It does not create a separate compatibility version system.

## Generated Target Expectations

`bridges/dominium/generators/targets.yaml` records future target classes only.

Q07 emits no real Dominium outputs. Future generated targets remain deferred and review-gated.

## Harness Enforcement

Harness v0 now checks required bridge files and boundary anchors structurally. It also reports Dominium target classes in `aide compile --dry-run` as plan-only metadata.

Harness does not parse full YAML, run Dominium proofs, mutate external repositories, or write real Dominium outputs.
