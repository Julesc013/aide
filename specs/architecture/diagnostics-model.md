# Diagnostics Model

## Purpose

Diagnostics are the stable machine-readable way for AIDE to report unavailable features, validation failures, transform issues, protocol problems, and advisory notes across all execution modes.

## Required fields

Each diagnostic should include:

- diagnostic id
- severity
- source
- user-facing message

It may also include:

- optional location or context
- machine-readable details or evidence
- suggested action or remediation hint
- metadata extension area

## Diagnostic identity

- ids should be stable and namespaced
- ids should identify the condition, not the display wording

Examples:

- `capability.unavailable`
- `request.missing-document-context`
- `transport.local-service-unreachable`

## Severity posture

Severity should remain small and stable. A conservative initial set is:

- `info`
- `warning`
- `error`

Later prompts may refine this only if implementation pressure justifies it.

## Source field

The source field identifies where the diagnostic originated, such as:

- a shared-core module
- the protocol layer
- a host adapter preflight step
- an execution-mode transport boundary

## Cross-mode rule

Diagnostics must work the same way across `embedded`, `cli-bridge`, and `local-service`.

Transport differences may change where a diagnostic originates, but they must not change the contract shape that the host adapter receives.
