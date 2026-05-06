# AIDE Outcome Controller

The Q16 Outcome Controller is an advisory-only, deterministic, repo-local
analysis layer.

It reads local signals from token ledgers, token summaries, verifier reports,
review packets, context artifacts, golden-task reports, validation evidence,
and controller ledger records. It writes compact outcome metadata and
recommendation reports under `.aide/controller/`.

It does not call models, providers, or network services. It does not mutate
prompts, policies, routes, generated context artifacts, source files, or
runtime behavior automatically.

## Outputs

- `outcome-ledger.jsonl`: metadata-only outcome records.
- `latest-outcome-report.md`: compact current signal summary.
- `latest-recommendations.md`: advisory recommendations with evidence source,
  expected benefit, risk level, next action, rollback condition, and
  `applies_automatically: false`.
- `failure-taxonomy.yaml`: failure classes used by the controller.

## Rule

Controller recommendations require a future queue item or explicit human
approval before implementation. Token optimization is invalid if golden tasks
fail or quality evidence is weakened.
