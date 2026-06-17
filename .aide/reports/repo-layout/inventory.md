# Repository Layout Inventory

- task_id: AIDE-BUILD-REPO-LAYOUT-INVENTORY-01
- generated_at: 2026-06-18
- source_commit: 376b151
- track: B
- report_only: true
- no_apply: true
- authorizes_implementation: false

## Current Repo Evidence

- Repo status: 5,136 files, 0 unknown classifications, 943 generated files,
  2,687 evidence files, and 608 orphan candidates.
- Root status: 22 roots, 3 mixed roots, 19 unknown or review-required roots,
  15 high-risk roots, 4,822 `keep` fates, 314 `unknown` fates, no-apply true.
- Refactor map: 0 move entries, 20 salvage entries, 0 aliases, 40 rewrite
  candidates, no-apply true.

## `.aide` Shape

Largest tracked `.aide` subtrees:

| Subtree | Tracked files |
| --- | ---: |
| `queue` | 2,253 |
| `export` | 829 |
| `reports` | 454 |
| `evals` | 348 |
| `policies` | 123 |
| `examples` | 108 |
| `scripts` | 54 |
| `release` | 44 |
| `refactors` | 41 |
| `upgrade` | 26 |
| `knowledge` | 26 |
| `tests` | 24 |
| `install` | 23 |
| `apply` | 22 |
| `repair` | 21 |
| `tools` | 18 |

`queue`, `export`, `reports`, and `evals` dominate the `.aide` footprint.
That is expected for a self-hosting control plane, but it makes generated and
evidence boundaries important.

## `core` Shape

Tracked `core` subtrees:

| Subtree | Tracked files |
| --- | ---: |
| `harness` | 11 |
| `contract` | 10 |
| `protocol` | 10 |
| `apply` | 8 |
| `compat` | 7 |
| `providers` | 7 |
| `gateway` | 6 |
| `knowledge` | 2 |
| `reconciler` | 2 |
| `control` | 1 |
| `runtime` | 1 |
| `sdk` | 1 |
| `tests` | 1 |

`core/protocol` remains small enough to stay flat for now. `core/runtime`,
`core/sdk`, and `core/control` are present as tiny stubs and should not be
expanded without queue authority.

## Duplicate Naming

Names shared by top-level roots and `.aide` subtrees:

- `evals`
- `scripts`

Names shared by `.aide` and `core` subtrees:

- `apply`
- `compat`
- `gateway`
- `knowledge`
- `protocol`
- `providers`
- `tests`

The duplicate names are not automatically wrong. They do require explicit
authority boundaries: `.aide` owns policy, state, schemas, reports, fixtures,
and evidence; `core` owns implementation helpers.

## Report Layout

`.aide/reports` currently has:

- 102 top-level report files.
- 52 report directories.
- 14 `-check` directories.
- 6 `-accept` directories.
- 6 `-acceptance` directories.
- 26 directories without `-check`, `-accept`, or `-acceptance` suffixes.

Flat check/accept report path references appear in 156 files with 365 matches.
Examples include `core/protocol/*`, `core/knowledge/okf_bundle.py`,
`core/reconciler/reconciler_reports.py`, queue task packets, task evidence,
PLANS, IMPLEMENT, and DOCUMENTATION.

## Protocol Split

`.aide/protocol` contains 8 schema files. `core/protocol` contains 10 tracked
implementation helper files.

This split is coherent:

```text
.aide/protocol = schema truth
core/protocol  = helper and validation implementation
```

Do not move `.aide/protocol` into `core`, and do not split `core/protocol` into
many packages until import churn or implementation complexity proves the need.

## Tracked `.aide/tmp`

Tracked `.aide/tmp` files currently exist under WorkUnit CLI mutation fixture
paths. They should be classified before any naming cleanup, but this inventory
does not move or rename them.
