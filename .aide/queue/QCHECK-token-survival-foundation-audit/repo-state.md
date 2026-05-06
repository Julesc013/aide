# Repository State

## Git

- Branch: `main`
- Start commit: `84b579ce8e50a38aecad23cd6a7408e3646bd8c9`
- Start worktree: clean
- Recent head: `84b579c docs: document provider adapter v0`
- Tracked files: 804
- Max-depth-3 file inventory: 417 files excluding `.git`

## Local State

- `.aide.local/`: absent and ignored.
- `.env`: absent.
- `secrets/`: absent.
- `git ls-files .aide.local .aide.local/ .env secrets`: no tracked paths.

## Generated Artifacts Touched By Audit Commands

Running approved report commands refreshed non-canonical generated reports:

- `.aide/context/repo-snapshot.json`
- `.aide/context/repo-map.json`
- `.aide/context/repo-map.md`
- `.aide/context/context-index.json`
- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-review-packet.md`
- `.aide/reports/token-ledger.jsonl`
- `.aide/reports/token-savings-summary.md`
- `.aide/evals/runs/latest-golden-tasks.json`
- `.aide/evals/runs/latest-golden-tasks.md`
- `.aide/controller/outcome-ledger.jsonl`
- `.aide/routing/latest-route-decision.json`
- `.aide/routing/latest-route-decision.md`
- `.aide/cache/latest-cache-keys.json`
- `.aide/cache/latest-cache-keys.md`
- `.aide/gateway/latest-gateway-status.json`
- `.aide/gateway/latest-gateway-status.md`
- `.aide/providers/latest-provider-status.json`
- `.aide/providers/latest-provider-status.md`

These are report artifacts, not product/runtime state.

## Top-Level Shape

The repo contains historical bootstrap records, shared runtime boot-slice code,
host research lanes, governance/inventory/matrices, `.aide/` self-hosting
contracts, Q00-Q20 queue packets, `core/gateway`, and `core/providers`.

## Audit Note

The repo is not product-ready. It is a pre-product self-hosting repo with a
working local token-survival control plane.
