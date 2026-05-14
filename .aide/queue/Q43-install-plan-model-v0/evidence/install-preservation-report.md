# Install Preservation Report

## Preservation Classes

Q43 preservation policy covers:

- target `.aide/memory/**`
- target `.aide/queue/**`
- target `.aide/context/latest-*`
- target `.aide/reports/**`
- target `.aide/evals/golden-tasks/**` target-specific tasks
- target `AGENTS.md` manual content outside managed sections
- target docs/canon/doctrine
- target existing tools
- target generated reports
- `.aide.local/**`, `.env`, secrets, raw prompts, and raw responses

## Source-State Exclusions

The install planner skips source-generated state as target truth, including:

- `.aide/context/latest-*`
- `.aide/reports/**`
- `.aide/repo/file-inventory.json`
- `.aide/roots/latest-*`
- `.aide/tools/latest-*`
- `.aide/refactors/current-*`
- `.aide/install/latest-*`

## Latest Preservation Evidence

- preservation report: `.aide/install/latest-preservation-report.md`
- preserved paths in plan: 1055
- target-specific files observed: 795
- mandatory migration candidates: 0
- source-generated install outputs are not exported as target truth.

## Caveats

- Q43 records preservation and conflict evidence only.
- Future target repos must generate their own install observations and plans.
- Migration remains future-gated and requires a mandatory reason plus review.
