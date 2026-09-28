# Portable Codex usage known-subtotal repair

Source base: local and remote `dev@ebe97afbf9bc1e80f3dc61e7988287e8e5f9a209`.
Scope: existing `job usage` parser and `test_efficiency_wait.py`; no model
request, new workspace or target mutation.

Two synthetic Codex JSONL cases reproduced incorrect accounting:

1. A completed turn with no cache/reasoning fields reported known subtotals
   of zero for those missing categories. Missing values must remain unknown.
2. A stream containing both completion and failure contributed its completed
   usage to known totals despite contradictory terminal evidence.

Red D-managed job `132f1d534deb4d4ba38ce73a5e31811e`, receipt SHA-256
`a5a3b11a3e5fecd661162d46b01222b29a6867ccdfd88fcb51d78f1fdf081701`,
ran 17 focused tests with exactly these two failures. Final green D-managed
job `75f5bc2c5653490990c1ca09d0bb6b71`, receipt SHA-256
`29d183c37d8879fa89b218537d70f27fce82f1a7c43267cbf0780d0ad32ccd40`,
ran all 17 successfully after the terminal-status assertion was added. The
earlier green job `766d6552` is intermediate evidence. All attempts retired
scratch and released their reservations. The source now marks a contradictory
terminal stream ambiguous,
excludes it from known subtotals and leaves categories with no valid source
value unknown. Independent `/root/stable_builder_repair_review` inspected the
exact source commit `46c51f7101c3d4d5018ea8c6b59b132e4bf558a0`, tree
`ad04943fb40999461fbc8c8298fa9ebccec35999`, on base
`ebe97afbf9bc1e80f3dc61e7988287e8e5f9a209` and returned **ACCEPT for
dev source integration**. The reviewer inspected the diff, tests, evidence,
Git object/state and whitespace check; the reviewer did not rerun the recorded
17 tests or conduct a live model turn. The verdict covers the parser change
only, not the existing release assets or final publication.

The accepted local 1.0.0 assets and `42672db9` effect remain bound to the
prior script bytes. This repair requires a later exact source-to-asset rebuild
and delivered-byte qualification before any changed release claim.
