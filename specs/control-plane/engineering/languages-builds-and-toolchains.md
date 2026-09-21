---
type: AIDE Engineering Specification
title: Languages, builds and toolchain profiles
description: Keep one reference controller, native adapters at native boundaries and exact deployment qualifications.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P05
  resource: urn:aide:source-package:a247c622c6987787cae0fe18ff9383bb202f185b7e99bf1ce22478d42412e36a
  title: AIDE-Spec-Overhaul-2026-09-20-R2(1)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P15
  resource: urn:aide:source-package:ddcd7109c50db5ad3bfe6693f5f09e52dd8c276280368af8105ab1b69458ea81
  title: AIDE-Spec-Overhaul-R2-2026-09-20(1).zip
- id: P18
  resource: urn:aide:source-package:d61e3fe58a17ae0b729d36519b23ba123de87571c55fcf0128f06e34e7c26723
  title: AIDE-Spec-Overhaul-v2-2026-09-20(1)(1).zip
- id: P19
  resource: urn:aide:source-package:dab4e0eb3f7c39b80e03cf84748ec9f88a3603da6edbdebd534628cce325f832
  title: AIDE-Spec-Overhaul-v2-2026-09-20(2).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: implementation and native toolchain owners
  applicability: implementation and build profiles
  requirement_ids:
  - UR-BUILD-01
  - UR-BUILD-02
  - UR-BUILD-03
  - UR-BUILD-04
  - UR-BUILD-05
  - UR-BUILD-06
  - UR-BUILD-07
---

# Languages, builds and toolchain profiles

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Keep one reference controller, native adapters at native boundaries and exact deployment qualifications.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Python remains the current reference implementation direction, not a promise that every legacy host runs modern Python. Introduce conventional packaging and managed interpreters through a characterized migration, not an unreviewed rewrite. Exact interpreter, dependency, optimization/JIT/free-threaded variant, invocation flags and import environment belong to a versioned runtime profile. This unification does not declare CPython 3.12 or 3.14 newly supported merely because a source pack recommends them.

PowerShell, POSIX shell and batch are useful launch and ecosystem adapters; do not duplicate durable policy and state semantics in each. Native C/C++/C#/Swift/Objective-C/TypeScript/Java/Delphi bindings serve the host boundaries they can actually support. CMake, MSBuild, Xcode, Cargo, Make and other project-native systems own their build graphs. AIDE describes, selects, invokes and records those systems.

Build configuration is a multidimensional tuple: controller, build host, target OS/architecture/ABI, compiler/runtime, configuration, dependencies, product profile, packaging and policy. Generate only locally valid presets from observed capabilities. Keep source, generated code, build outputs, caches and installed products distinct. Performance changes to interpreter or native accelerator need matched workload and differential correctness evidence.

## Interface and data boundary

Controller profile; interpreter/executable/dependencies; host/build/target tuple; native build authority; source/preset inputs; output paths; ABI; packaging/signing; observed capabilities.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-BUILD-01 — Qualified controller runtime

Authoritative controller execution MUST bind an exact supported runtime/dependency/invocation profile rather than arbitrary PATH Python.

### UR-BUILD-02 — Separate support matrices

Controller runtime, build host, target artifact and user-facing host support MUST be separate matrices.

### UR-BUILD-03 — Native build authority

AIDE MUST preserve native build/test/package systems as authoritative domain implementations.

### UR-BUILD-04 — Explicit build tuple

Build evidence MUST identify source, toolchain, target tuple, configuration, dependencies, commands and artifacts.

### UR-BUILD-05 — No duplicated scripting core

Shell and platform scripts MUST remain bounded adapters unless separately designated as the owning semantic implementation.

### UR-BUILD-06 — Interpreter variants separate

Free-threaded, JIT, alternate interpreter and native accelerator variants MUST be qualified independently with differential correctness and workload evidence.

### UR-BUILD-07 — Installed behavior tests

Controller packaging qualification MUST test installed entrypoints in clean environments, not only imports from the source checkout.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-BUILD-01` | The ambient interpreter changes. | AIDE resolves the admitted runtime or refuses with a clear compatibility diagnostic. |
| `UC-BUILD-02` | A modern controller produces a legacy-target binary. | Legacy target support does not imply that the controller runs on that legacy OS. |
| `UC-BUILD-03` | A target uses MSBuild-specific semantics. | AIDE invokes the qualified native binding rather than recreating the build graph by heuristics. |
| `UC-BUILD-04` | Two targets share a preset display name. | Their build identities remain distinguishable. |
| `UC-BUILD-05` | A wrapper begins implementing a second policy evaluator. | Architecture checks flag competing semantics. |
| `UC-BUILD-06` | A faster interpreter variant is selected. | It does not inherit the reference profile’s qualification automatically. |
| `UC-BUILD-07` | The package omits a required module. | Installed-artifact tests fail before release acceptance. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
