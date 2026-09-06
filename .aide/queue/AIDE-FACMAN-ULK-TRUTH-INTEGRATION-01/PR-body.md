Correct the ULK closeout to distinguish historical August main/dev synchronization from the September tracking-ref observations. The checker rejects inherited shared-tree and edited-candidate equality claims after workspace hygiene changed dev.

The final candidate is 76d93a0e81e5b8f9391123780157402e27ff486f, with reviewed tree cf1ab68a3695cfbc8a5947cc5444b7cca620c883. The main-to-dev ancestry synchronization adds no file changes to the reviewed correction.

Validation: 46 Python tests, 15 strict checks and all eight hosted Linux/macOS/Windows x64/Win32 checks passed. Independent review verified historical/current trees and ancestry. Runtime, ABI and package behavior are unaffected.

Work-Item: ULK-1.9.1-CURRENT-TRUTH-CLOSEOUT-01
Evidence-Ref: docs/release/checkpoints/ulk-1-9-1-current-truth-closeout-01.md