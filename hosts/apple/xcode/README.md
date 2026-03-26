# Apple Xcode

This directory is the host-family scaffold for Apple Xcode. Child directories represent the documented `xcodekit` source-editor lane and the broader AIDE `companion` fallback lane.

Exact Xcode-family coverage is tracked in `inventory/ide-versions.yaml` and the matrices, not in folder names.

P12 makes the lane split explicit:

- `xcodekit`: blocked structural native proof with embedded editor-marker intent recorded
- `companion`: runnable `cli-bridge` fallback proof for older or broader workflows

This keeps the public Apple-native lane visible without pretending that native Xcode runtime verification occurred outside macOS or Xcode.
