# No Forbidden Operations

The build preserved these false facts:

- Dominium command invoked: false.
- Host runtime started: false.
- Host SDK implemented: false.
- Workbench started or implemented: false.
- Bridge runtime started or implemented: false.
- Service, database runtime, and transport started: false.
- Network call performed: false.
- Provider/model called: false.
- Worker executed: false.
- PatchTransaction applied: false.
- Preview/apply/rollback performed: false.
- Target repository mutated: false.
- Branch/worktree created: false.
- GitHub mutation performed: false.
- Release or promotion performed: false.

Unsupported CLI verbs `run`, `invoke`, `execute`, `apply`, `write`, `sync`, `push`, `serve`, `connect`, and `dispatch` are registered refusals, not hidden execution paths.
