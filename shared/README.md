# AIDE Shared Core

`shared/` is the future home for reusable AIDE logic that can be defended as genuinely cross-host.

It exists to hold:

- shared feature orchestration
- transport-agnostic request and response handling
- reusable transforms
- diagnostics normalization
- settings resolution
- stable machine-readable schemas
- shared CLI and local-service surfaces

`shared/` does not exist to absorb host UI wiring, host packaging rules, or IDE-specific runtime glue. Those remain in `hosts/`.

The subtree defined in this prompt is structural only. It establishes durable homes for future implementation without claiming that the shared core is already implemented.
