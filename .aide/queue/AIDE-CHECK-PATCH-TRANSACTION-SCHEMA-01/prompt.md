# AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01

Check-only independent review of the minimal PatchTransaction protocol slice.

The task verifies the completed `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`
source chain, schema/helper/report behavior, artifact digest, path-scope
safety, lifecycle and authority boundaries, deterministic projection,
source immutability, CLI boundary, report consistency, and task evidence.

Allowed writes are limited to this check task packet and evidence,
`.aide/reports/patch-transaction-check/**`, `.aide/queue/index.yaml`,
`PLANS.md`, and `IMPLEMENT.md`.

The check must not repair implementation, modify PatchTransaction schema/helper
or tests, regenerate build reports to conceal mismatches, apply patches,
approve transactions, mutate target files, activate profiles, admit or trust
subjects, implement AdapterManifest, ContextPack v2, runtime, Test Broker,
Service, Commander, Workbench, provider/model/Gateway/network/GitHub behavior,
branch/worktree automation, release, promotion, or target repository apply.

If no material finding exists, recommend
`AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01`.

If a material repairable defect exists, recommend
`AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.
