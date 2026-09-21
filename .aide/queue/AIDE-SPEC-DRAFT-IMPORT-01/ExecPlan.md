# ExecPlan: Explicit Draft Specification Import

## Objective

Place the remaining control-plane design chapters in the repository as
navigable drafts without confusing file presence with semantic adoption.

## Scope

- Verify the external specs-only package and its source transformations.
- Apply only `specs-only.patch` against the inspected `e4ab82e9` baseline.
- Add 34 draft chapters plus a draft index and exact import manifest.
- Modify only the control-plane README among existing specification files.
- Update live convergence and documentation indexes within this WorkUnit.

## Non-Goals

- No runtime, queue-schema, policy, model, provider, release, or branch merge work.
- No bulk adoption of `UR-*` or `UC-*` aliases.
- No import of private archives, generated registers, tools, baselines, or patches.
- No claim that proposed acceptance designs were executed.

## Progress

- [x] Verify ZIP integrity and safe extraction outside the checkout.
- [x] Review package instructions and verifier source.
- [x] Pass package reconstruction, patch round-trip, and disposable tests.
- [x] Run live preflight and classify its Windows line-ending refusal.
- [x] Confirm the actual specs-only patch applies cleanly.
- [x] Apply the exact patch.
- [x] Update live status and documentation indexes.
- [x] Validate preservation, draft posture, links, and changed paths.
- [x] Prepare the bounded increment for commit and push.

## Validation

Use the package verifier, package tests, direct Git patch checks, exact hashes
for preserved adopted contracts, requirement/case counts, relative-link checks,
queue validation, and staged-diff inspection.

## Recovery

Before commit, `git apply --reverse --check` can prove the patch boundary. The
external package and existing Git baseline retain the exact input. No unrelated
dirty file may be staged or rewritten.
