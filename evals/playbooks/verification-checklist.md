# Verification Checklist

## Structural Existence Checks

- Confirm required files and directories exist.
- Confirm required manifests, catalogs, or records are present for the scoped work.

## Schema Checks

- Confirm machine-readable files follow their documented structural shape.
- Record any unresolved ambiguity rather than silently normalizing it.

## Documentation Consistency Checks

- Confirm docs, manifests, matrices, and catalogs agree on scope and status.
- Confirm no file claims implementation or coverage that does not exist.

## Smoke Verification

- If smoke checks are in scope, record the target lane, environment, and expected evidence before running.
- If smoke checks are not possible yet, record `deferred`, `blocked`, or `unverifiable` honestly.

## Blocker Capture

- Record any missing implementation, environment, media, or tooling blockers explicitly.
- Distinguish blocker-driven delays from an intentional deferment.

## Evidence Recording

- Record the command output, review notes, logs, screenshots, or archival references that justify the result.
- Do not record a passing outcome without concrete evidence.

## Matrix And Catalog Updates

- Update matrices or catalogs only when the evidence justifies the posture change.
- Keep current-state claims conservative.
