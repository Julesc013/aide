# AIDE Inventory

`inventory/` is the machine-readable source of truth for stable ids, seed records, canonical enums, and exact version records that will be expanded later. It is structural and factual. It is not a governance area and it is not a roadmap.

## File Roles

- `vendors.yaml`: canonical vendor ids.
- `products.yaml`: canonical product ids tied to vendors.
- `ide-families.yaml`: canonical host-family ids tied to products.
- `adapter-technologies.yaml`: canonical compatibility-technology ids.
- `os-families.yaml`: canonical operating-system family ids.
- `toolchains.yaml`: seed toolchain-category ids.
- `enums.yaml`: canonical enums consumed by matrices and manifests.
- `ide-versions.yaml`: future exact IDE version records.
- `os-versions.yaml`: future exact OS version records.

## Inventory Versus Governance

Governance documents define policy and operating law. Inventory files define ids, records, and enumerations used by matrices, manifests, and later implementation work.

## Exact Version Claims

Exact version claims belong in `ide-versions.yaml`, `os-versions.yaml`, later inventory expansions, and matrix/manifests that reference those ids. Exact version coverage does not belong in folder names.

## Unknown Values

Use `null`, empty lists, or explicit markers such as `unknown`, `unverified`, `placeholder`, and `deferred` when research is incomplete. Do not invent values to satisfy shape.

## Operating Rule

Inventory records must describe reality as currently known. Structural placeholders are allowed when clearly marked. Aspirational claims are not.
