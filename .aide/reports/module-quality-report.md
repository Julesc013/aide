# Module Quality Report

## Largest Source Or Tool Files

- .aide/scripts/aide_lite.py: 779489 bytes (AIDE Lite)
- core/harness/commands.py: 40268 bytes (AIDE harness)
- core/harness/generated_artifacts.py: 25577 bytes (AIDE harness)
- core/gateway/gateway_status.py: 21545 bytes (gateway skeleton)
- shared/core/boot_slice.py: 17508 bytes (unknown)
- core/compat/version_registry.py: 10756 bytes (compatibility baseline)
- shared/protocol/models.py: 9912 bytes (unknown)
- core/providers/registry.py: 9788 bytes (provider metadata and contracts)
- core/providers/status.py: 9023 bytes (provider metadata and contracts)
- scripts/aide-queue-run: 6644 bytes (AIDE harness)
- shared/core/dispatcher.py: 6013 bytes (unknown)
- shared/config/boot_slice.py: 4725 bytes (unknown)
- hosts/metrowerks/codewarrior/companion/run_boot_slice.py: 3833 bytes (host adapters)
- hosts/metrowerks/codewarrior/ide-sdk/run_boot_slice.py: 3826 bytes (host adapters)
- hosts/microsoft/visual-studio-mac/companion/run_boot_slice.py: 3735 bytes (host adapters)
- hosts/microsoft/visual-studio/extensibility/run_boot_slice.py: 3734 bytes (host adapters)
- hosts/microsoft/visual-studio/vsix-v1/run_boot_slice.py: 3711 bytes (host adapters)
- hosts/apple/xcode/companion/run_boot_slice.py: 3703 bytes (host adapters)
- hosts/microsoft/visual-studio/com-addin/run_boot_slice.py: 3698 bytes (host adapters)
- core/harness/aide_harness.py: 3571 bytes (AIDE harness)

## High Dependency Count Candidates

- .aide/scripts/aide_lite.py: large_module_candidate, missing_doc_candidate, mixed_purpose_candidate, orphan_candidate, public_surface_missing_doc_candidate, reuse_candidate

## Mixed Purpose Candidates

- .aide/scripts/aide_lite.py: Inspect references and owner before any future refactor; do not delete from Q38 evidence.

## Owner Summary

- AIDE Git workflow: 16
- AIDE GitHub advisory: 8
- AIDE Lite: 23
- AIDE changelog preview: 10
- AIDE context compiler: 12
- AIDE control plane: 107
- AIDE cross-repo export pack: 279
- AIDE evals: 116
- AIDE governance: 38
- AIDE harness: 15
- AIDE intent compiler: 11
- AIDE repo intelligence: 21
- AIDE self-hosting queue: 496
- bridge records: 17
- compatibility baseline: 14
- documentation reference: 48
- gateway skeleton: 6
- host adapters: 68
- provider metadata and contracts: 7
- unknown: 277

## Caveats

- module findings are first-pass candidates
- Q38 does not refactor or extract helpers
