# Feature Model

## What a feature is

A feature is a stable unit of shared AIDE behavior that a host adapter can request from the shared core.

A feature is not a menu label, host-specific command id, or packaging artifact. It is the cross-host behavior behind those surfaces.

## Feature identity

- each feature uses a stable feature id
- ids should be durable, lowercase, and contract-oriented
- ids should describe behavior rather than one host's UI label

Examples of feature-oriented ids:

- `session.identify-host`
- `editor.transform-selection`
- `workspace.inspect-project`

## Feature requirements

Each feature must declare:

- the minimum required capability level
- the context it requires, such as document, selection, or workspace data
- any support-mode or execution-mode restrictions if those are real architectural constraints
- expected outputs such as edits, actions, artifacts, or diagnostics

## Feature and capability relationship

Capability levels are lane ceilings. Features consume those ceilings.

- a feature whose minimum requirement is `L2` must not be reported as available on a lane that can only currently provide `L1`
- a lane with a theoretical target of `L3` may still report a feature unavailable if its current implementation state is below that level

## Host-lane availability

The same feature may be:

- available on one native lane
- companion-only on another
- unavailable on a third because the host contract does not expose enough context

That is expected. Feature parity is a shared-behavior goal, not a promise of identical host depth.

## Feature manifests

Later prompts should record feature manifests as machine-readable files aligned to `shared/schemas/feature-manifest.schema.yaml`.

A manifest should declare:

- feature identity
- summary and intended outputs
- minimum capability
- required contexts
- allowed support modes or execution modes where relevant
- deferred or unavailable notes when the feature cannot be made universal
