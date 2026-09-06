Correct the ULK closeout to distinguish the historical August main/dev synchronization from the September tracking-ref observations. Dev now includes workspace hygiene, so the checker rejects inherited shared-tree and edited-candidate equality claims.

Source: `151a18f9f67af1a1ede17bda72641155d22106e5`; tree: `cf1ab68a3695cfbc8a5947cc5444b7cca620c883`.

Validation: all 46 Python tests and 15 strict checks passed. Independent review verified the exact historical/current trees and ancestry, with no runtime, public-header, ABI, package-layout or authority changes. Current GitHub Checks must pass on this corrected head before merge.

Work-Item: ULK-1.9.1-CURRENT-TRUTH-CLOSEOUT-01

Evidence: [current-truth checkpoint](docs/release/checkpoints/ulk-1-9-1-current-truth-closeout-01.md). Normal merge-commit integration is authorized by the current full Beta1 execution request; publication and consumer adoption remain separate.
