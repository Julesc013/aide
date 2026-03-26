# Microsoft Open Questions

## Unresolved

- Pre-2010 Windows Visual Studio extensibility is still represented by the `com-addin` umbrella. Current official source coverage is sufficient to justify the umbrella, but not yet sufficient to split every legacy contract family cleanly.
- The exact operational boundary between `vsix-v2-vssdk` and `extensibility` inside the late Visual Studio 2022 era remains intentionally conservative. Microsoft supports both families, and AIDE should not assume feature parity between them.
- Visual Studio for Mac extension packaging and API differences across the 2017, 2019, and 2022 lines are not fully cataloged here.
- This prompt does not model Marketplace policy, signing, or packaging mechanics for Microsoft extension artifacts beyond the architectural lane mapping.

## Deferred

- A legacy-focused Microsoft prompt can decide whether the `com-addin` umbrella needs narrower archival lanes.
- A later implementation prompt should determine whether AIDE's Windows Visual Studio reference lane is `vsix-v2-vssdk` or `extensibility`, based on actual host APIs, verification cost, and shared-core fit.
- A later archival prompt can decide whether the Visual Studio for Mac `companion` lane should stay macOS-only or gain a broader cross-host posture.

