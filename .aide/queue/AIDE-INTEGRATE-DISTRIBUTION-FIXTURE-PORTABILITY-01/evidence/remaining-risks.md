# Remaining Risks

- Independent exact-commit review is pending.
- Eight symlink/FIFO cases remain unqualified on this Windows token; reparse
  attribute and hardlink refusal cases passed.
- Portable artifact provenance must be refreshed after integration against the
  exact new `dev` commit.
- Real-target lifecycle apply and production rollback remain outside this fixture-only task.
