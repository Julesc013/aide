# QFIX-06 ExecPlan: QCHECK-04 Warning Remediation

## Objective

Fix safely actionable QCHECK-04 warnings and rerun validation while preserving
AIDE review gates and publication boundaries.

## Scope

- Refresh generated artifact manifest if the harness confirms only the manifest
  is stale.
- Reduce repeated deterministic selftest and fixture setup cost where safe.
- Record which QCHECK-04 warnings were fixed, which remain review/policy gates,
  and which are deliberately deferred.
- Rerun focused validation.

## Boundaries

- Do not mark Q36-Q48 as `passed`; they remain review-gated.
- Do not push, tag, publish, upload, mutate branches, call GitHub APIs, or call
  providers/models/network.
- Do not mutate Dominium or Eureka.
- Do not implement Q49.

## Plan

1. Inspect QCHECK-04 warnings and generated compile plan.
2. Create this bounded remediation packet.
3. Refresh generated manifest if the compile plan remains safe.
4. Rerun validation and lifecycle checks.
5. Update evidence, stop at `needs_review`, and commit.

## Progress

- [x] QCHECK-04 warnings inspected.
- [x] Compile dry-run confirmed generated manifest replacement is the safe fix.
- [x] Remediation packet created.
- [x] Generated manifest refreshed.
- [x] AIDE Lite selftest repeat-cost patch applied.
- [x] Minimal fixture setup trimmed to reduce raw unittest discovery cost.
- [x] Export pack, release bundle, and release draft regenerated.
- [x] Validation rerun.
- [x] Evidence updated.
- [ ] Commit created.
