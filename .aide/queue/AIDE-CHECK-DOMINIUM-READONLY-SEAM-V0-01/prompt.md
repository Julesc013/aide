# AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01

Create and process `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01`.

Use `.aide/queue/index.yaml` as canonical AIDE queue truth. Re-read the live repository before writing anything.

This is a milestone-sized CHECK task. Perform a complete independent adversarial review of `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01`. Do not repair defects in this task.

Allowed writes are limited to the check task directory, `.aide/reports/dominium-readonly-seam-v0-check/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

The check must go beyond rerunning the builder suite. It must independently verify repository identity, source revision/freshness binding, selected inputs, Git object and symlink safety, snapshot and bundle digest integrity, manifest/count/cardinality, ReferenceID and cross-reference closure, ownership, authority roles, record-specific contracts, public schema usefulness, diagnostic/refusal registry projections, capability allowlists, event semantics, compatibility claims, TOML/default-path portability, negative fixture replayability, conformance result independence, demo evidence integrity, no-write proof, and no-network/provider/worker proof.

If no material defect exists, recommend exactly `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`.

If one or more bounded material defects exist, recommend exactly `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01`.

Stop at `needs_review`.
