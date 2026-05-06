# Q21 Prompt

Implement Cross-Repo Pack Export / Import v0 for a portable AIDE Lite Pack.

The phase depends on QFIX-01 and QFIX-02 and must not mutate real Eureka or
Dominium repositories. It must create deterministic stdlib-only export/import
tooling, local fixture validation, documentation, and evidence. It must exclude
source repo identity, queue history, generated context, reports, local state,
secrets, raw prompts, raw responses, route/cache/gateway/provider latest state,
and outcome ledgers from the portable pack.

Stop at `needs_review`.
