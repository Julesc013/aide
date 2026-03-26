# CodeWarrior Boot-Slice Smoke Run

## Scope

P13 committed legacy host-family lanes only.

This run records the first CodeWarrior host-lane boot-slice wave and separates runnable archival-native proof from runnable companion fallback proof without pretending native in-host SDK loading was verified.

## Commands Run

- `py -3 -B -m unittest discover -s shared/tests -t .`
- `py -3 hosts\metrowerks\codewarrior\ide-sdk\run_boot_slice.py --verify --pretty`
- `py -3 hosts\metrowerks\codewarrior\companion\run_boot_slice.py --verify --pretty`

## Runnable Proofs

- `metrowerks.codewarrior.ide-sdk`: passed a runnable archival-native `cli-bridge` `L1` report-first proof.
- `metrowerks.codewarrior.companion`: passed a runnable `cli-bridge` `L1` companion fallback proof for unresolved or non-native CodeWarrior workflows.

## Structural And Deferred Native Evidence

- `metrowerks.codewarrior.ide-sdk`: structural native-adjacent metadata exists in `plugin-target.yaml`, but no honest in-host IDE SDK or COM automation loading was runtime-verified in the current environment.

## Deferred

- Native in-host CodeWarrior IDE SDK loading and COM automation wiring remain deferred to a reproducible historical environment.
- The optional `boot.slice.editor-marker` proof for `ide-sdk` remains deferred until active-document capture is available.
- Broader project-aware companion workflows remain deferred even though the fallback proof is runnable.
- No Microsoft or Apple host-lane work is covered by this run.

## Evidence References

- `hosts/metrowerks/codewarrior/ide-sdk/boot_slice_request.json`
- `hosts/metrowerks/codewarrior/ide-sdk/boot_slice_response.json`
- `hosts/metrowerks/codewarrior/ide-sdk/plugin-target.yaml`
- `hosts/metrowerks/codewarrior/ide-sdk/run_boot_slice.py`
- `hosts/metrowerks/codewarrior/companion/boot_slice_request.json`
- `hosts/metrowerks/codewarrior/companion/boot_slice_response.json`
- `hosts/metrowerks/codewarrior/companion/run_boot_slice.py`
