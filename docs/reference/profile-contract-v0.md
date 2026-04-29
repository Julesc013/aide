# Profile Contract v0

## Purpose

Profile/Contract v0 makes the AIDE repository self-describing for queue-driven work. It records what this repository declares, requires, allows, exposes, owns, and defers.

The Profile is declarative. Harness is later executable machinery.

## Source Of Truth

Canonical Q03 contract records live under `.aide/`:

- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/components/catalog.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/policies/**`
- `.aide/tasks/catalog.yaml`
- `.aide/evals/catalog.yaml`
- `.aide/adapters/catalog.yaml`
- `.aide/compat/**`

The filesystem queue under `.aide/queue/` remains canonical for task execution state. Queue status is not product doctrine.

## File Layout

| Path | Meaning |
| --- | --- |
| `.aide/profile.yaml` | AIDE repo identity, lifecycle, public model, implemented reality, future intent, and source-of-truth pointers. |
| `.aide/toolchain.lock` | Minimal lock record for Contract/Profile v0 posture. |
| `.aide/components/catalog.yaml` | Component declarations for Core Contract, Harness, Compatibility, Control, deferred Runtime and SDK, deferred Hosts, Dominium Bridge, docs, and queue. |
| `.aide/commands/catalog.yaml` | Implemented queue helper scripts and planned Harness commands. |
| `.aide/policies/ownership.yaml` | Path ownership and stricter-policy-wins rules. |
| `.aide/policies/generated-artifacts.yaml` | Generated artifact boundary; generated downstream outputs remain planned for Q05. |
| `.aide/policies/compatibility.yaml` | Compatibility claim policy pointer; Q06 owns baseline reconciliation. |
| `.aide/policies/validation-severity.yaml` | Severity vocabulary for future Harness validation. |
| `.aide/tasks/catalog.yaml` | Queue item intent and task type declarations; live status remains in `.aide/queue/`. |
| `.aide/evals/catalog.yaml` | Minimal self-hosting eval declarations. |
| `.aide/adapters/catalog.yaml` | Metadata-only target agent families. |
| `.aide/compat/**` | Schema version and migration baseline placeholders. |
| `core/contract/shapes/**` | Markdown documented shapes for v0 records. |

## Field Meanings

- `schema_version`: version identifier for the file's declared shape.
- `profile_contract_version`: version identifier for the Q03 contract set.
- `status`: current posture. Use explicit values such as `implemented`, `partial`, `planned`, `deferred`, `not_implemented`, or `metadata-only`.
- `owned_paths`: paths a component conceptually governs. Ownership is not permission to move files.
- `non_goals`: scope that must remain out of the current component or queue item.
- `verification_posture`: how this record is currently checked.

## Implemented Now

Q03 implements:

- declarative Profile/Contract v0 records under `.aide/`
- documented v0 shapes under `core/contract/shapes/`
- source-of-truth reference documentation
- root documentation pointers
- queue evidence and review status

## Planned Or Deferred

Q03 does not implement:

- Q04 Harness commands
- Q05 generated downstream artifacts
- Q06 compatibility baseline or migration engine
- Q07 Dominium Bridge implementation
- Runtime, Hosts, Commander, Mobile, IDE extension implementation, provider adapters, app surfaces, package automation, or autonomous service logic

## Generated Outputs

Generated downstream artifacts are outputs, not canonical source-of-truth records. Q05 owns deterministic generated artifact boundaries and drift evidence. Q03 only records the policy boundary.

## Queue Relationship

The Profile describes repo contract posture. The queue describes work execution state. A future Harness should validate both, but Q03 does not create that executable Harness.
