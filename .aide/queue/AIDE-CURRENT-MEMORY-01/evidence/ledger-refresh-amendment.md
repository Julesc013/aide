# Derived ledger refresh needed by the memory correction

The preserved first doctor/validate results fail on the existing source-input
binding. A read-only call to capability_ledger_evidence_validity reports STALE,
source_inputs_changed, with exactly .aide/memory/project-state.md. The old memory
is an input to this advisory classification; changing it must invalidate the old
ledger. Do not bypass the guard or describe the original run as PASS.

Amend this documentation child's allowlist with only the four paths written by
existing write_capability_ledger: ledger JSON/Markdown, evidence bindings JSON and
command-status Markdown. The accompanying task.yaml lists the exact paths.
After exact review, run existing capability ledger once, preserve its output,
verify CURRENT binding and inspect classification changes. Then rerun doctor and
full structural validation; existing global historical review-ref warning stays
explicit. These are deterministic report/structural commands, not tests or worker
allocations. No generator/validator/policy change, runtime claim or release effect.

The frozen amendment-source map binds the actual prose, task, first failures,
CLI, seeds/current source refs and four prior report preimages. This amendment
permits candidate refresh only. Later exact source and integration-effect review
still precedes commit, promotion, push or task retirement.
