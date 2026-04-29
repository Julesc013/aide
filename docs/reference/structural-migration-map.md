# Structural Migration Map

## Purpose

This map connects the bootstrap-era physical repository layout to the Q02 target structure. Q02 does not move source files. It creates additive skeletons and records conceptual ownership boundaries.

Move status values:

- `keep`: stay physically where they are for the current reboot stage.
- `shim`: future compatibility shim may be needed before any move.
- `future move`: possible later migration after explicit review and validation.
- `candidate`: possible later track, not committed by Q02.
- `deferred`: intentionally not active in Q02.

## Current-To-Target Map

| Current Physical Location | Conceptual Home | Move Status | Notes |
| --- | --- | --- | --- |
| `shared/` | future `core/contract/`, `core/harness/`, `core/runtime/`, and `core/tests/` depending on subarea | keep | Existing Python shared-core boot slice, CLI bridge, schemas, and tests remain in place. No migration in Q02. |
| `shared/schemas/` | `core/contract/` | keep | Bootstrap-era schemas remain contract evidence until Q03 or later reviewed work. |
| `shared/tests/` | `core/tests/` and `core/harness/` | keep | Existing tests remain in place to preserve imports and fixtures. |
| `shared/cli/` | `hosts/cli/` and `core/harness/` support | shim | Future CLI migration may need compatibility shims; Q02 does not move it. |
| `hosts/apple/**` | `hosts/extensions/xcode/` plus preserved bootstrap proofs | keep | Apple proof lanes remain factual bootstrap-era evidence. |
| `hosts/microsoft/**` | `hosts/extensions/visualstudio/` plus preserved bootstrap proofs | keep | Microsoft proof lanes remain factual bootstrap-era evidence. |
| `hosts/metrowerks/**` | `hosts/extensions/later/` plus preserved bootstrap proofs | keep | CodeWarrior proof lanes remain factual bootstrap-era evidence and are not recategorized physically. |
| `hosts/templates/**` | future host template surface | keep | Existing templates remain in place; Q02 does not broaden template systems. |
| `governance/**` | `core/control/` and constitution references | keep | Repository law remains authoritative in its bootstrap-era location. |
| `inventory/**` | `core/compat/` and `core/control/` | keep | Canonical ids and version records remain in place. |
| `matrices/**` | `core/compat/` and `core/control/` | keep | Support, capability, feature, platform, test, and packaging posture remain in place. |
| `research/**` | `core/compat/` and design-mining inputs | keep | Source-backed research remains evidence, not implementation. |
| `environments/**` | `core/control/` and `core/compat/` | keep | Environment control-plane records remain in place. |
| `labs/**` | target public `labs/` plus Compatibility/Harness evidence | keep | Lab records remain the place for prototypes, blockers, and archival work. |
| `evals/**` | `core/harness/`, `core/compat/`, and `core/control/` | keep | Eval models and run records remain in place. |
| `packaging/**` | `core/control/` and deferred release/artifact track | keep | Packaging control-plane records remain deferred and unmoved. |
| `scripts/**` | future `hosts/cli/`, `core/harness/`, and `core/control/` support | keep | Queue helpers and maintenance scripts remain in place. |
| `.agents/**` | portable skills and maintained agent guidance | keep | Repo-local skills remain operational guidance. |
| `.aide/**` | canonical self-hosting contract, queue, status, policy, and evidence | keep | `.aide/queue/` remains canonical. |
| `docs/**` | target public `docs/` | keep | Reboot documentation families remain under docs. |
| `core/**` | target AIDE Core skeleton | future move | Q02 creates README-only skeletons; later queue items may populate them. |
| `hosts/cli/**` | target CLI Host skeleton | future move | Q02 creates README-only skeletons; existing scripts remain in place. |
| `hosts/service/**` | target Service Host skeleton | deferred | No service is implemented in Q02. |
| `hosts/commander/**` | target Commander Host skeleton | deferred | No Commander app is implemented in Q02. |
| `hosts/extensions/**` | target extension-host skeleton | future move | Q02 creates placeholders only; existing proof lanes remain in place. |
| `bridges/**` | target AIDE Bridges skeleton | future move | Q02 creates README-only skeletons. |
| `bridges/dominium/**` | Dominium Bridge skeleton | deferred | Baseline bridge work is Q07. |
| `bridges/dominium/xstack/**` | Dominium-local XStack profile skeleton | deferred | XStack remains Dominium-local and is not implemented in Q02. |

## Migration Rule

Future moves require a queue item with explicit allowed paths, compatibility or shim strategy, import-preservation validation, evidence, and review approval. Until then, conceptual ownership does not imply physical relocation.
