# Apple Platform Reach

Primary sources: [Xcode overview](https://developer.apple.com/xcode), [Xcode support matrix](https://developer.apple.com/support/xcode), [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/).

## Facts

- Xcode is macOS-hosted.
- Apple's current Xcode and support pages describe Xcode as the toolset for building apps for Apple platforms.
- Apple's current support matrix and requirements pages explicitly cover iOS, iPadOS, macOS, tvOS, watchOS, and visionOS in the Xcode 16 and Xcode 26 era.

## Inventory and matrix implications

- `inventory/os-families.yaml` needs `ios`, `ipados`, `tvos`, `watchos`, and `visionos` to represent Xcode's verified target-platform envelope at a high level.
- `matrices/platform-reach.yaml` should keep `host_os_families` for Xcode at `macos`.
- `potential_target_os_families` should be high-level Apple platform families only. This matrix is not the place for exhaustive SDK ceilings, minimum deployment tables, or per-patch host constraints.

## Inferences

- The target-platform list applies to the Xcode family context, not to where an AIDE extension binary runs. A native Xcode extension still runs on macOS because Xcode itself is macOS-hosted.
- The same target-family envelope can be used for both the `xcodekit` and `companion` rows because both lanes exist to assist work inside a macOS-hosted Xcode environment.

## Unresolved

- Historical target-platform reach for very old Xcode families is deliberately deferred; the current matrix only records the high-level Apple-platform envelope that is architecturally relevant now.
