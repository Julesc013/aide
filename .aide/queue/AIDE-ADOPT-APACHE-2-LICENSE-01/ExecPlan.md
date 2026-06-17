# ExecPlan: AIDE-ADOPT-APACHE-2-LICENSE-01

## Objective

Adopt a standard permissive legal-document packet for AIDE using Apache-2.0 as
the default repository license.

## Scope

Allowed writes:

- `.aide/queue/AIDE-ADOPT-APACHE-2-LICENSE-01/**`
- `.aide/queue/index.yaml`
- `LICENSE.md`
- `NOTICE.md`
- `LICENSING.md`
- `GENERATED_OUTPUTS.md`
- `TRADEMARKS.md`
- `LICENSE_SUMMARY.md`
- `README.md`
- `CONTRIBUTING.md`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`

## Plan

1. Verify live repo state and queue/bypass policy.
2. Use the supplied permissive licensing drafts and official Apache-2.0 source
   references as inputs.
3. Add the final root legal docs.
4. Update README, contributor guidance, documentation index, planning log,
   execution log, and queue index.
5. Record evidence for changed files, validation, no forbidden operations, and
   remaining risks.
6. Validate and stop at `needs_review`.
7. Commit the scoped legal-doc change separately from unrelated work.

## Non-Goals

No runtime, protocol-schema, support-tier, capability-level, release,
publication, branch, GitHub, provider/model, target-repository, trademark
registration, CLA, or generated-output source-truth changes are authorized.

## Exit Criteria

- Apache-2.0 legal packet exists in root docs.
- README and CONTRIBUTING match the new licensing posture.
- Documentation, planning, implementation, queue, and evidence records are
  updated.
- Validation is recorded.
- The task status is `needs_review`.
