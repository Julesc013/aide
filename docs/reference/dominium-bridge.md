# Dominium Bridge Baseline

## Purpose

Dominium Bridge is the first AIDE Bridge baseline. It defines how Dominium can later consume AIDE as a pinned, portable repo-native layer while keeping XStack as Dominium's strict local governance and proof profile.

Q07 implements only AIDE-side bridge metadata and validation posture. It does not modify the Dominium repository, emit real Dominium generated outputs, implement Dominium product semantics, or add Runtime, Host, provider, app, release, or autonomous service behavior.

## Scope

The Q07 bridge baseline includes:

- bridge metadata under `bridges/dominium/bridge.yaml`;
- adoption guidance for a future Dominium repo task;
- structural validation expectations;
- an XStack boundary and portable mapping;
- a Dominium/XStack profile overlay;
- stricter review, proof, and generated-artifact policy overlays;
- generator target expectation metadata, with real Dominium outputs deferred;
- compatibility and pinning rules that reference the Q06 Compatibility baseline.

## Non-Goals

Q07 does not:

- change any external Dominium repository;
- define Dominium application, product, or Runtime semantics;
- implement XStack internals or proof execution;
- make XStack a generic AIDE product layer;
- generate Dominium `AGENTS.md`, `.agents/skills/**`, Claude, Codex, OpenHands, or bridge-pack outputs;
- add provider, model, browser, network, release, packaging, IDE, Commander, Mobile, or host behavior;
- replace `.aide/profile.yaml` or any AIDE canonical source-of-truth record.

## Stack Ordering

The intended ordering is:

1. AIDE portable Core records: Contract, Harness, Compatibility, queue policy, generated-artifact rules, and evidence.
2. Dominium Bridge: AIDE-side metadata, overlays, generated-target expectations, compatibility pinning, and validation declarations.
3. XStack: Dominium-local strict governance and proof profile above AIDE.
4. Dominium repository: a future consumer outside Q07 scope.

AIDE remains portable. Dominium may later consume AIDE, but AIDE does not become Dominium-owned or Dominium-shaped.

## XStack Relationship

XStack remains Dominium-local. The bridge may map portable AIDE concepts to XStack expectations, but it must not claim that AIDE implements XStack or that XStack is generic AIDE doctrine.

The boundary is recorded in:

- `bridges/dominium/xstack/scope.md`;
- `bridges/dominium/xstack/portable-mapping.yaml`.

## Adoption Modes

Q07 recommends `pinned-managed-repo-layer` for near-term Dominium adoption.

In this mode, a later Dominium task pins an AIDE commit, reviewed bundle, or future release artifact and consumes the bridge records as a portable layer. Q07 itself does not create that pin in Dominium and does not write into any Dominium repo path.

Other modes remain deferred:

- `template-mode`: candidate only, because it risks copying stale policy into Dominium.
- `bridge-pack-mode`: deferred until packaging and release evidence exists.
- `release-bundle-mode`: deferred until AIDE has reviewed release automation.

## Validation Expectations

Harness v0 performs only structural bridge checks:

- required bridge files exist;
- `bridge.yaml` identifies `aide.dominium-bridge.v0`;
- XStack files say Dominium-local and strict;
- policy overlays declare `base_policy_relation: stricter-than-aide`;
- generated target metadata declares `emits_outputs: false`;
- compatibility pinning references `aide.compat-baseline.v0`;
- the bridge does not require external Dominium repository mutation.

These checks do not parse full YAML and do not execute Dominium proofs.

## Compatibility And Pinning

Bridge pinning is recorded in `bridges/dominium/compatibility.yaml`.

The bridge uses AIDE string identifiers and references the Q06 Compatibility baseline. It does not create a separate incompatible version system.

Dominium adoption later should pin one of:

- an AIDE commit hash;
- a reviewed AIDE bundle;
- a future AIDE release artifact after release automation exists.

Pin changes require review and evidence.

## Generated Artifact Expectations

`bridges/dominium/generators/targets.yaml` records future target classes only. Q07 does not emit real Dominium outputs.

Future target classes may include:

- Dominium `AGENTS.md` managed sections;
- Dominium `.agents/skills/**`;
- Claude, Codex, and OpenHands guidance files if a later task enables them;
- bridge adoption reports or manifests.

All real output generation remains deferred and review-gated.

## Future Work

Future queue items may:

- review Q07;
- decide whether bridge metadata should become a generated target input;
- add stronger bridge validation after full YAML/schema strategy exists;
- create a Dominium-side adoption task in the Dominium repo;
- define bridge-pack or release-bundle behavior after packaging and release evidence exists.

Those future tasks must preserve the boundary that AIDE is portable and XStack remains Dominium-local.
