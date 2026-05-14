# Preservation Boundary Report

Q46 preserves by default:

- target `.aide/memory/**`;
- target `.aide/queue/**`;
- target `.aide/evidence/**`;
- target `.aide/evals/golden-tasks/**`;
- generated target context and reports unless a future reviewed apply phase
  marks them regenerable;
- `.aide/git/latest-*`, `.aide/repo/*.json`, `.aide/roots/latest-*`, and
  `.aide/tools/latest-*`;
- `AGENTS.md` manual content outside managed sections;
- docs/canon/doctrine and project governance;
- existing repo tools;
- `.aide.local/**`, `.env`, secret-like paths, raw prompts, and raw responses;
- unknown-ownership files.

Ownership evidence inputs:

- `.aide/install/latest-ownership-ledger.example.json`
- `.aide/install/latest-install-plan.json`
- `.aide/upgrade/latest-upgrade-plan.json`
- `.aide/repair/latest-repair-plan.json`
- current repo state

Rollback uses missing or ambiguous ownership as a blocker/manual-review reason.
Uninstall treats unknown ownership as preserve/manual review. Neither command
plans blanket `.aide` removal.
