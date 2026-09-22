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
