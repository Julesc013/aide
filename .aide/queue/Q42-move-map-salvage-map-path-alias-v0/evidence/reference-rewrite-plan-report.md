# Reference Rewrite Plan Report

## Policy And Schemas

- Policy: `.aide/policies/reference-rewrite.yaml`
- Plan schema: `.aide/refactors/reference-rewrite-plan.schema.json`
- Entry schema: `.aide/refactors/reference-rewrite-entry.schema.json`

The policy permits only candidate reference rewrite planning in Q42. It scans
markdown links, inline path references, import references, script/config
references, and generated maps as planning inputs.

## Current Output

- JSON: `.aide/refactors/reference-rewrite-plan.json`
- Markdown: `.aide/refactors/reference-rewrite-plan.md`
- Entries: 40
- `no_apply`: true
- `files_rewritten`: false

The current plan records candidate references from Q37 doc-link and dependency
data. Entries remain conservative hints and do not include active rewrites.

## No-Rewrite Proof

`refactor rewrite-plan` reported `files_rewritten: false`; `validate-map`
confirmed all rewrite entries have `apply_allowed: false` and are not
`future_applied`.
