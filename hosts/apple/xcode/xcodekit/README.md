# Xcode XcodeKit Lane

This directory is the `xcodekit` compatibility-technology lane for `apple.xcode`.

It represents Apple's documented Xcode Source Editor extension surface through XcodeKit. Exact version coverage is tracked in inventory and matrices.

P12 adds an explicit blocked structural boot-slice record for this lane:

- `boot_slice_request.json` records the intended `embedded` `L2` editor-marker request
- `extension-target.yaml` records the native-adjacent extension-target shape
- `blocked-proof.md` records why a real source-editor proof is not yet honest in the current environment

This lane still lacks a verified macOS or Xcode environment, a containing-app packaging path, and a verified embedded bridge from XcodeKit into the shared core. The blocked record preserves the required native `L2` target instead of collapsing it into the companion fallback lane.
