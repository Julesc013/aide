# Microsoft Visual Studio

This directory is the Windows Visual Studio host-family scaffold. Child directories represent compatibility technologies rather than version buckets: a legacy native umbrella, two VSIX generations, and the newer VisualStudio.Extensibility lane.

P11 adds three first-wave Windows proofs:

- `com-addin`: runnable degraded `cli-bridge` proof
- `vsix-v1`: runnable degraded `cli-bridge` proof
- `extensibility`: runnable degraded `cli-bridge` proof with local-service deferred

The `vsix-v2-vssdk` lane remains explicitly blocked because its accepted first proof requires a native `L2` editor path that is not honest to claim in the current environment.
