# Prompt

Implement `X-OS-02 - AIDE Capability Reality Ledger v0` in the source AIDE repository only.

The full raw user prompt is intentionally not embedded here. This queue packet records the bounded execution scope, acceptance criteria, forbidden operations, and evidence requirements needed to implement the task without storing raw prompt bodies as canonical task truth.

Key objective: add deterministic, standard-library-only AIDE Lite report commands for capability status, scan, ledger generation, overclaim reporting, and validation over the X-OS-00 capability reality policy and X-OS-01 report-only command foundation. The commands must classify capability claims conservatively and must not apply, mutate branches, mutate target repos, publish releases, call providers/models, use network, execute repairs, execute tasks, or implement a scheduler/worker/runtime/provider surface.
