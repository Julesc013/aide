# Remaining Risks

- The first independent review requested changes after reproducing a Windows
  8.3 alias mutation. The repair passes locally but exact-commit rereview is
  pending.
- Eight symlink/FIFO cases remain unqualified on this Windows token; reparse
  attribute and hardlink refusal cases passed.
- Portable artifact provenance must be refreshed after integration against the
  exact new `dev` commit.
- Real-target lifecycle apply and production rollback remain outside this fixture-only task.
