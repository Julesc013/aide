# Prompt

Implement `X-OS-01 - AIDE Task OS Report-Only Commands` in the source AIDE repository only.

The full raw user prompt is intentionally not embedded here. This queue packet records the bounded execution scope, acceptance criteria, forbidden operations, and evidence requirements needed to implement the task without storing raw prompt bodies as canonical task truth.

Key objective: add deterministic, standard-library-only AIDE Lite report commands for task status/classification, repair/requeue/resume plans, blocker status/classification, wave status/plan, and checkpoint status/plan over X-OS-00 Task OS contracts. The commands must write report-only evidence and must not apply, mutate branches, mutate target repos, publish releases, call providers/models, use network, execute repairs, or execute tasks.
