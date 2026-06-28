# Remaining Risks

- The profile is public-metadata-only and may miss local ignored, generated, or untracked state.
- Local clean/dirty state cannot be verified until a local MIR checkout path is configured.
- Lua syntax and Factorio validation cannot run until executables are configured.
- Source version `1.2.10` is ahead of latest observed GitHub release `1.2.9`; this may be expected but requires future release-flow review.
- Ownership classification is a candidate profile, not accepted local target truth.
- Shadow apply, real target apply, release generation, publication, branch/worktree automation, and automatic version bumps remain non-capabilities.
