# ExecPlan: Delivered Pack Customization

## Objective and scope

Implement one bounded missing consumer journey on the accepted combined dev:
project-owned configuration, a direct local edit, a conflicting upstream
update, deterministic preservation explanation, and explicit local feedback.
Change only this WorkUnit's allowlist. No live target, hosted, provider, or
publication effect.

## Dependencies and progress

- [x] Start from observed dev `3bdeb220` with release and target source integrated.
- [x] Inspect import authority, ownership, receipt, and conflict behavior.
- [x] Add exact-byte rationale binding and explanation without changing apply authority.
- [x] Add opt-in local feedback with no automatic telemetry.
- [x] Run source tests and adversarial cases: 27-case suite and two focused rechecks passed.
- [x] Regenerate and qualify final portable bytes in disposable consumers.
- [ ] Record source/artifact evidence, prevalidate closeout, and integrate if reviewed and accepted.
- [x] Detect that an existing pending-intent dry run could mutate recovery
  state; supersede `37daa862` before review or dev integration.
- [x] Repair read-only recovery preview and reserve project rationale metadata
  against pack payloads; focused adversarial tests pass.
- [x] Rebuild exact bytes and qualify final candidate `8cad56c0` in extracted ZIP consumers.
- [x] Close a Windows case/trailing-dot alias of the reserved project-owned
  metadata path; the checksummed alias refusal test passes.

## Verification and recovery

Test preservation and conflict-first behavior with two pack versions, direct
edits, matching/stale/malformed rationale, and feedback absent/present. Then
qualify an extracted archive consumer and run the current release generator's
post-commit replay. Fix forward on the task branch; do not replace current
release machinery with older branch output.
