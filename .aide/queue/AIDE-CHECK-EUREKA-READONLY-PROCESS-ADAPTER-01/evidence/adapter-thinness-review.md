# Adapter Thinness Review

The Eureka adapter is domain-specific around:

- repository identity;
- selected command and digests;
- preflight;
- state probe binding;
- Eureka JSON decoder;
- result/refusal mapping;
- report/evidence projection.

The actual registered process launch path remains owned by
`RegisteredProcessExecutionProvider v0`. The adapter does not expose a broad
command dispatch CLI.
