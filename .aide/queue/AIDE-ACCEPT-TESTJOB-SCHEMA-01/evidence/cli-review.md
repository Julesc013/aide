# CLI Review

Result: PASS.

Accepted:

- `test-job status` reports metadata-only TestJob boundaries.
- `test-job project --source accepted-artifacts` writes additive projections and reports no source mutation.
- `test-job validate` reports `PASS`.
- Unsupported `test-job submit`, `test-job run`, `test-job retry`, and `test-job summarize` subcommands fail closed with argparse exit code 2.

No execution-capable TestJob command is accepted by this review.
