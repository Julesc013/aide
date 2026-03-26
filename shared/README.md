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

P10 introduces a narrow bootstrap implementation for the first boot slice under:

- `shared/core/`
- `shared/protocol/`
- `shared/diagnostics/`
- `shared/config/`
- `shared/cli/`
- `shared/tests/`

This runtime is intentionally small. It implements only deterministic request and response handling, capability reporting, unavailable or deferred reporting, the boot-slice editor-marker transform, and a host-agnostic CLI bridge for `cli-bridge` mode proof. It does not implement host adapters, local-service lifecycle management, packaging, or later capability levels.
