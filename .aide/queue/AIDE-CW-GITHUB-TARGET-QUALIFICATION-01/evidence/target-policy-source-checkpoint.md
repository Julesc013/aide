# Target-Policy Source Checkpoint

## Exact Source

- `core/runtime/integration_broker/github_target_policy.py` SHA-256:
  `b3a08360180f96ec5f2608e478eee7fb22b4876c31b0f4340d1e276c251e2b5b`.
- `.aide/scripts/tests/test_continuous_worker_github_observation.py` SHA-256:
  `2d8306b731940b832df0f6ea5f7991e13e8acb6d6ea3ecf6acda397ea0f293ea`.

## Exact Review Inputs

- Desired policy SHA-256:
  `cc7447efefa8de3fef797a289f8eb0a78514955e5449cb9d9348e6bab70ff157`.
- Current observation SHA-256:
  `caa808af49186fbb7937e20d1fb4de2f575667c5142ff07c8af19c33aa8668af`.
- Blocked review plan SHA-256:
  `e466b58b7db42a1938624f8d0683342ce9244d60352b148be6638cb6a25ca865`.
- Policy digest:
  `db1b1ad6e96d287386ad5d99c600b938c3e65dc12123a98954106d58bab68b7f`.
- Observation digest:
  `907688c5defff9615e8f8d5f0bac9d9e39e8d3bf6522ceb7f2813c51df134798`.
- Plan digest:
  `5c243ac74ff1deff1780debe97e5e0ec1dcfa42653d2898c37db84b54ef15d7d`.

## Result

The implementation and local fixtures pass. The live plan is `blocked`, has
zero operations, and is not authorized for apply. Exact broker principal and
workflow/check identities are unresolved. No workflow, setting, credential,
branch, pull request, merge, tag, release, or hosted race was changed or run.
