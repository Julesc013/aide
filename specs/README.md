# AIDE Specifications

`specs/` contains AIDE's human-authored product and technical contracts. It
defines desired behavior. It does not, by itself, prove that behavior is
implemented, qualified, activated, supported, or authorized for a particular
operation.

## Layout

| Area | Purpose | Current posture |
|---|---|---|
| [Control plane](control-plane/README.md) | Product scope and cross-cutting contracts for durable work, authority, outcomes, execution, evidence, and lifecycle behavior. | Adopted incrementally; implementation and qualification are tracked separately. |
| [Architecture](architecture/README.md) | Shared-core and host-adapter architecture, including accepted ADRs. | Preserved durable architecture. |
| [Boot slice](boot-slice/README.md) | The original identify/invoke/report host slice and its rollout records. | Preserved implementation-facing baseline; not a claim of current product completeness. |

Future specification families should extend these areas rather than creating a
second root, version-range directory, or competing master specification.

## Authority

- Specifications own reviewed desired behavior.
- `.aide/` policy and queue records own repository law, permission, and current work.
- Source and tests establish implementation facts.
- Exact evidence establishes observed qualification within its recorded scope.
- Release records establish support and publication claims.

These authorities are related but not interchangeable. A specification `MUST`
does not grant execution permission, and a passing test does not silently adopt
new product requirements.

## Source Adoption

Private review archives stay outside the repository. Material enters this tree
only through a source-traceable disposition that says whether it was retained,
adapted, split, superseded, deferred, rejected, or left unresolved. See the
[unified specification status](../docs/reference/unified-spec-status.md) for the
current convergence boundary.

This directory is distinct from governance law, research inputs, inventory
facts, support matrices, implementation source, and generated evidence.
