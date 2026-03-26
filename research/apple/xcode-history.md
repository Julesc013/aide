# Xcode History

Primary sources: [Xcode support matrix](https://developer.apple.com/support/xcode), [Xcode overview](https://developer.apple.com/xcode), [Xcode Release Notes](https://developer.apple.com/documentation/xcode-release-notes/), [What's New in Xcode - Archive](https://developer.apple.com/library/archive/documentation/Xcode/Conceptual/WhatsNewXcode-Archive/Articles/Introduction.html), [Xcode Release Notes - Archive](https://developer.apple.com/library/archive/documentation/Xcode/Conceptual/RN-Xcode-Archive/Chapters/Introduction.html), [Using an Existing Xcode 3 Project](https://developer.apple.com/library/archive/documentation/IDEs/Conceptual/Xcode4TransitionGuide/ExistingProject/ExistingProject.html), [64-Bit Transition Guide](https://developer.apple.com/library/archive/documentation/Darwin/Conceptual/64bitPorting/building/building.html), [TN2456](https://developer.apple.com/library/archive/technotes/tn2456/_index.html).

## Major-family table

| Record id | Family label | Apple source basis | Host OS | Primary AIDE lane | Vendor posture |
| --- | --- | --- | --- | --- | --- |
| `xcode1` | Xcode 1 | Archived 64-Bit Transition Guide refers to "Xcode 1.0 and later." | `macos` | `companion` | unverified |
| `xcode2` | Xcode 2 | Xcode 4 transition material says Xcode 4 reads and builds projects created in Xcode 2.1. | `macos` | `companion` | unverified |
| `xcode3` | Xcode 3 | Xcode 4 transition material is written for Xcode 3 users and migration. | `macos` | `companion` | unverified |
| `xcode4` | Xcode 4 | Xcode 4 Transition Guide and archived What's New chapter. | `macos` | `companion` | unverified |
| `xcode5` | Xcode 5 | Archived What's New chapter for Xcode 5. | `macos` | `companion` | unverified |
| `xcode6` | Xcode 6 | Archived What's New chapter and TN2456 recent-tools table. | `macos` | `companion` | unverified |
| `xcode7` | Xcode 7 | Archived What's New chapter and TN2456 recent-tools table. | `macos` | `companion` | unverified |
| `xcode8` | Xcode 8 | TN2456 recent-tools table; AIDE uses this as the first `xcodekit`-mapped family. | `macos` | `xcodekit` | unverified |
| `xcode9` | Xcode 9 | TN2456 recent-tools table. | `macos` | `xcodekit` | unverified |
| `xcode10` | Xcode 10 | Current release-notes taxonomy continues to enumerate Xcode 10 as a major family. | `macos` | `xcodekit` | unverified |
| `xcode11` | Xcode 11 | Current release-notes taxonomy continues to enumerate Xcode 11 as a major family. | `macos` | `xcodekit` | unverified |
| `xcode12` | Xcode 12 | Current release-notes taxonomy continues to enumerate Xcode 12 as a major family. | `macos` | `xcodekit` | unverified |
| `xcode13` | Xcode 13 | Current release-notes taxonomy and Apple requirements pages still refer to Xcode 13 explicitly. | `macos` | `xcodekit` | unverified |
| `xcode14` | Xcode 14 | Apple support matrix lists Xcode 14.3.1 in the older-versions section. | `macos` | `xcodekit` | unverified |
| `xcode15` | Xcode 15 | Apple support matrix lists Xcode 15.x in the older-versions section. | `macos` | `xcodekit` | unverified |
| `xcode16` | Xcode 16 | Apple support matrix lists Xcode 16.x and Upcoming Requirements keeps it as the submission floor until April 28, 2026. | `macos` | `xcodekit` | supported |
| `xcode26` | Xcode 26 | Apple current Xcode page, support matrix, and Upcoming Requirements all treat Xcode 26 as the current family. | `macos` | `xcodekit` | supported |

## Facts

- Apple's archived material is enough to verify Xcode 1, Xcode 2, Xcode 3, Xcode 4, Xcode 5, Xcode 6, and Xcode 7 as real major families without inventing date-range directory names or patch-level catalogs.
- Apple's current support and release-note pages are enough to verify Xcode 8 through Xcode 16 and Xcode 26 as distinct major families relevant to current AIDE planning.
- Apple's official source set available here does not justify backfilling Xcode 17 through Xcode 25 as distinct major families.

## Inferences

- AIDE maps Xcode 1 through Xcode 7 to the `companion` lane because the current official Apple source set used here does not establish a modern public in-host extension surface for those families.
- AIDE maps Xcode 8 and later to the `xcodekit` lane because Apple's public XcodeKit and Xcode Source Editor documentation define the native surface that still matters for current planning.

## Unresolved

- This source set does not provide a Microsoft-style lifecycle table for older Xcode families, so most historical `vendor_lifecycle_state` values remain `unverified`.
- The exact first shipping breakpoint for the public XcodeKit/source-editor-extension era is tracked as a research note, not as a claim of patch-level certainty in machine-readable inventory.
