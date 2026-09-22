# Validation

Exact combined source merge: `7aab31bc1bc747484d80c662d20e218bb93d1f5b`.

- PASS WITH SKIPS: 125 focused portability tests; 117 passed and eight skipped.
- PASS WITH SKIPS: 156 adjacent `test_aide_distribution*.py` tests; 148 passed and eight skipped.
- PASS: `py -3 -B .aide/scripts/aide_lite.py test`.
- PASS: source and merge commit-message checks.
- PASS: `git diff --check`.
- EXPECTED FAIL: canonical `validate` and `pack-status` report only tracked
  portable-pack provenance at `b3e5c7aa` rather than candidate `7aab31bc`.

The eight skips are explicit host limitations: the normal Windows token cannot
create symlinks and Windows does not expose the FIFO fixture used by that test.
Hardlink and Windows reparse-attribute refusal cases passed. No skipped test is
reported as qualified.

The changed `core/distribution` modules are not in the current aide-lite export
payload. The tracked pack still requires a commit-bound post-integration refresh
because its manifest intentionally identifies the exact source commit.

No non-disposable target, network, credential, GitHub setting, branch policy,
main ref, tag, upload, or release publication was changed.

## Windows 8.3 Review Repair

The first independent review reproduced a high-severity failure: an active
`LONGFI~1.TXT` alias reached and changed its long-name target. That
`REQUEST_CHANGES` record is preserved in `independent-review.md` and
`independent-review.json`.

- PASS WITH SKIPS: 126 repaired focused tests; 118 passed and eight skipped.
- PASS: the new native Windows test obtained the actual short name, observed
  `path_collision_refused` from both `safe_join` and operation execution, and
  proved the long-name file remained byte-for-byte unchanged.
- PASS WITH SKIPS: 157 adjacent distribution tests; 149 passed and eight
  skipped, zero failures.
- PASS: `py -3 -B .aide/scripts/aide_lite.py test`.
- EXPECTED FAIL: canonical `validate` retains exactly two projections of the
  known stale portable-pack source provenance at `b3e5c7aa`.
- NOT RUN: non-disposable target mutation, privileged symlink creation, hosted
  effects, main promotion, tagging, upload, or release publication.

Superseding independent rereview passed exact commit `64979977922ae8a493646df5858d0bd7f4459cd0`
and tree `c7474c29bbd84dfce6fc08c892544da045b6db3a`. The reviewer additionally
exercised active nested-parent and nested-leaf 8.3 aliases, exact long-name
compatibility, source ancestry/blob preservation, both test suites, AIDE Lite
test, commit checks, and diff checks.

## Dev Integration

The exact reviewed candidate was integrated into `dev` by two-parent commit
`bb689227c6a65292f4728d7ae0f8759c22e77bd3`, with reviewed candidate
`6cb0a9ac8856a4e733b1d48ef2a86d50badb5d22` preserved as its second parent.

- PASS WITH SKIPS: 126 focused portability tests; 118 passed and eight skipped.
- PASS WITH SKIPS: 157 adjacent distribution tests; 149 passed and eight skipped.
- PASS: `py -3 -B .aide/scripts/aide_lite.py test`.
- PASS: corrected integration commit message policy and `git diff --check`.
- PENDING: regenerate and validate commit-bound portable artifacts from the
  landed clean source commit.

No main ref, tag, upload, GitHub Release, non-disposable consumer, or machine
configuration was changed by this integration.
