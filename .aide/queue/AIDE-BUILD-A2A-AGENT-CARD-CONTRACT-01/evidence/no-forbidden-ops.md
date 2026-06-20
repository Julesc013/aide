# No Forbidden Operations

No forbidden operation was performed.

Preserved non-capabilities:

- no live A2A endpoint;
- no agent registration;
- no task delegation;
- no authentication or credential resolution;
- no worker execution;
- no provider/model/network call;
- no Host Contract, Dominium Bridge, Workbench, Runtime, or Service;
- no PatchTransaction apply;
- no branch/worktree, GitHub, release, promotion, or target-repository mutation.

Unsupported CLI probes for `start`, `serve`, `register`, `delegate`, `send`,
`connect`, and `authorize` fail closed through argparse.
