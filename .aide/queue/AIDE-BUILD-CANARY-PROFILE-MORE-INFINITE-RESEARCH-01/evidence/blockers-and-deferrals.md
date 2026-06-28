# Blockers And Deferrals

Result is `PARTIAL` because:

- no local MIR checkout path is configured or found;
- local target clean/dirty state cannot be verified;
- local ignored/untracked files cannot be classified;
- Lua executable configuration is unknown;
- Factorio executable/headless validation is not configured.

Deferred:

- local target profile check;
- MIR validation profile;
- MIR UpdatePlan preview;
- shadow update canary;
- reviewed branch/worktree update;
- release/package generation or publication.
