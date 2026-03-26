# AIDE Support Policy

## Purpose

This document defines the support contract for AIDE. Support statements must use explicit support tiers, state labels, support modes, and capability ceilings. Unsupported parity claims are forbidden.

## Support Tiers

- `T0` Uncommitted: named for architectural awareness or future inventory only; no implementation, maintenance, or release promise.
- `T1` Research: host or contract has been studied and documented; no runnable integration is required.
- `T2` Experimental: lane is bootstrapping; partial behavior may exist, breakage is expected, and workflow guarantees are minimal.
- `T3` Limited Support: bounded workflows are intentionally supported with a declared capability ceiling and explicit verification scope.
- `T4` Maintained Support: declared workflows are maintained with repeatable verification and planned release handling.
- `T5` Reference Support: highest repository commitment; lane acts as a reference path for shared-core assumptions, support discipline, and release rigor.

## State Labels

- `planned`: named target with no completed research yet.
- `researched`: constraints and contract are documented, but no runnable lane is claimed.
- `booting`: scaffold or integration work is underway, but reliable loading is not yet claimed.
- `loads`: lane loads and identifies the host or contract surface; this generally aligns with capability level `L0`.
- `usable`: bounded real workflows are available and intentionally supported within the declared ceiling.
- `shipping`: lane is releasable for the scope it actually claims.
- `frozen`: lane is intentionally no longer advancing except for archival or critical maintenance handling.

## Support Modes

- `native`: integration uses a current in-host extension surface.
- `legacy-native`: integration uses a historical or deprecated but still host-native extension contract.
- `companion`: integration is provided by an out-of-process or adjacent tool rather than by a fully native in-host extension surface.
- `archival`: integration exists for preservation, inspection, or constrained historical operation rather than active feature growth.

## Coverage And Naming Rules

- All exact version claims belong in inventory files, matrix files, and metadata/manifests, not in architectural folder names.
- Directory names are based on compatibility technology or host contract, not exact versions, version ranges, or date eras.
- Release artifacts may contain exact host versions when that improves clarity for produced deliverables.

## Capability Ceiling Rule

- Support tier and support mode do not imply a universal capability ceiling.
- Different hosts may top out at different capability levels because their extension technologies and automation surfaces differ.
- A lane may honestly top out below `L4` and still be valid.

## Honesty Rules

- Terms such as supported or unsupported are incomplete on their own and should be avoided unless paired with tier, state, mode, and capability context.
- Unsupported parity claims are forbidden.
- Native parity must never be inferred from shared-core reuse alone.
- Claims must be scoped to the host family, contract surface, and verified capability ceiling actually achieved.
