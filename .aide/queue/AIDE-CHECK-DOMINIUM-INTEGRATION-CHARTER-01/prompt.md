# Prompt

Create and process `AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01`.

Use `.aide/queue/index.yaml` as canonical AIDE queue truth. Re-read live repository state before writing anything.

This is a check-only task. Do not repair the charter, modify Dominium, implement the read-only seam, materialize downstream implementation tasks, or begin any Host Contract, Bridge, Workbench, service, runtime, provider, worker, network, preview, apply, or mutation work.

The main adversarial focus is the charter's pinned Dominium snapshot:

- pinned local Dominium HEAD: `c92b386027890c1bbf14aef6eaafe0357b7b03dd`
- pinned local branch status: `main`, clean, behind `origin/main` by 24

Independently compare the pinned snapshot with current authoritative Dominium `main` using read-only remote inspection. Do not fetch into, reset, merge, rebase, pull, or update the local Dominium checkout.

Stop at `needs_review`. Recommend `AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01` if no material issue exists; otherwise recommend `AIDE-BUILD-DOMINIUM-INTEGRATION-CHARTER-REPAIR-01`.
