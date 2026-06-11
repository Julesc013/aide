# Unfinished Work

## Finished

- Temp-only apply for `install-managed-section` / `apply-temp`.
- Postimage hash verification.
- Manual content preservation verification.
- Rollback-compatible record emission.
- `latest-run.json`, `latest-verify.json`, `verify.json`, and Markdown reports.
- Future and unfinished work reports.

## Partially Finished

- Report fields are protocol-shaped for this slice, but no full public schema or conformance suite is introduced.
- Path-jail behavior is tested for parent traversal, absolute paths, and symlink escape where the platform permits symlink creation.

## Not Attempted By Design

- full kernel
- service
- Commander
- provider adapters
- branch/worktree allocator
- supervisor
- async test broker
- target repo apply
- active repo apply
- rollback execution
- uninstall execution
- promotion
- release
- OpenTelemetry
- SARIF
- SPDX
- CycloneDX
- SLSA
- in-toto
- OpenAPI

## Blockers

- No blocking missing file or unavailable command remains for this bounded slice.
- Broader architecture work is blocked by design until independent review approves this slice.
