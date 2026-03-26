# Apple Boot-Slice Smoke Run

## Scope

P12 Apple host-family lanes only.

This run records the first Apple host-lane boot-slice wave and separates the runnable companion fallback proof from the explicitly blocked native XcodeKit lane.

## Commands Run

- `py -3 -B -m unittest discover -s shared/tests -t .`
- `py -3 hosts\apple\xcode\companion\run_boot_slice.py --verify --pretty`

## Runnable Proofs

- `apple.xcode.companion`: passed a runnable `cli-bridge` `L1` companion fallback proof for older or broader Xcode workflows outside the native XcodeKit lane.

## Structural And Blocked Proofs

- `apple.xcode.xcodekit`: structural blocked proof only. The lane keeps its intended `embedded` `L2` editor-marker target, but no honest macOS or Xcode runtime verification was available in the current environment.

## Deferred

- Native Xcode Source Editor command loading, containing-app packaging, and editor-surface marker verification remain deferred for the `xcodekit` lane.
- Broader project-aware companion workflows remain deferred even though the Apple companion fallback proof is runnable.
- No Microsoft or CodeWarrior host-lane work is covered by this run.

## Evidence References

- `hosts/apple/xcode/xcodekit/boot_slice_request.json`
- `hosts/apple/xcode/xcodekit/extension-target.yaml`
- `hosts/apple/xcode/xcodekit/blocked-proof.md`
- `hosts/apple/xcode/companion/boot_slice_request.json`
- `hosts/apple/xcode/companion/boot_slice_response.json`
- `hosts/apple/xcode/companion/run_boot_slice.py`
