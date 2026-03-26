# Microsoft Boot-Slice Smoke Run

## Scope

P11 Microsoft host-family lanes only.

This run records the first Microsoft host-lane boot-slice wave and separates runnable cli-bridge proofs from explicitly blocked native or archival-native lanes.

## Commands Run

- `py -3 -m unittest discover -s shared/tests -t .`
- `py -3 hosts\microsoft\visual-studio\com-addin\run_boot_slice.py --verify --pretty`
- `py -3 hosts\microsoft\visual-studio\vsix-v1\run_boot_slice.py --verify --pretty`
- `py -3 hosts\microsoft\visual-studio\extensibility\run_boot_slice.py --verify --pretty`
- `py -3 hosts\microsoft\visual-studio-mac\companion\run_boot_slice.py --verify --pretty`

## Runnable Proofs

- `microsoft.visual-studio.com-addin`: passed a degraded `cli-bridge` `L1` report-first proof.
- `microsoft.visual-studio.vsix-v1`: passed a degraded `cli-bridge` `L1` report-first proof.
- `microsoft.visual-studio.extensibility`: passed a degraded `cli-bridge` `L1` report-first proof while leaving the richer modern host shape deferred.
- `microsoft.visual-studio-mac.companion`: passed a runnable companion `cli-bridge` fallback proof and explicitly reports the native Mac lane as blocked.

## Structural And Blocked Proofs

- `microsoft.visual-studio.vsix-v2-vssdk`: structural blocked proof only. The lane keeps its intended `embedded` `L2` editor-marker target, but no honest native VSSDK environment was available for runtime verification.
- `microsoft.visual-studio-mac.monodevelop-addin`: structural blocked proof only. The lane keeps its archival-native `L1` target, but no reproducible Visual Studio for Mac environment was available for runtime verification.

## Deferred

- Native package loading, shell registration, and editor-surface verification remain deferred for the Windows `com-addin`, `vsix-v1`, and `extensibility` lanes.
- The `vsix-v2-vssdk` lane still lacks the required embedded `L2` editor-marker proof.
- The `visual-studio-mac.monodevelop-addin` lane still lacks any honest runtime add-in verification because the host is retired and archival assets are not present here.
- No Apple or CodeWarrior host-lane work is covered by this run.

## Evidence References

- `hosts/microsoft/visual-studio/com-addin/boot_slice_request.json`
- `hosts/microsoft/visual-studio/com-addin/boot_slice_response.json`
- `hosts/microsoft/visual-studio/vsix-v1/boot_slice_request.json`
- `hosts/microsoft/visual-studio/vsix-v1/boot_slice_response.json`
- `hosts/microsoft/visual-studio/vsix-v2-vssdk/boot_slice_request.json`
- `hosts/microsoft/visual-studio/vsix-v2-vssdk/blocked-proof.md`
- `hosts/microsoft/visual-studio/extensibility/boot_slice_request.json`
- `hosts/microsoft/visual-studio/extensibility/boot_slice_response.json`
- `hosts/microsoft/visual-studio-mac/monodevelop-addin/boot_slice_request.json`
- `hosts/microsoft/visual-studio-mac/monodevelop-addin/blocked-proof.md`
- `hosts/microsoft/visual-studio-mac/companion/boot_slice_request.json`
- `hosts/microsoft/visual-studio-mac/companion/boot_slice_response.json`
