# Next Task Prompt

`AIDE-CHECK-REFERENCE-ID-SCHEME-01`

Review the completed `AIDE-BUILD-REFERENCE-ID-SCHEME-01` slice.

Scope:

- Check `.aide/protocol/aide-reference-id.schema.json`.
- Check `core/protocol/reference_id.py`.
- Check `.aide/scripts/aide_lite.py` `reference-id` command registration.
- Check `.aide/scripts/tests/test_aide_reference_id_scheme.py`.
- Check `.aide/reports/reference-id/**`.
- Check `.aide/queue/AIDE-BUILD-REFERENCE-ID-SCHEME-01/**`.

Required review points:

- Reference IDs are stable `aide://<kind>/<id>` identities.
- File paths remain locators, not identity.
- Existing predecessor artifacts are not mutated by projection.
- Unknown optional future kinds warn.
- Unknown required future kinds fail closed.
- The slice does not implement EventRecord, OKF, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, runtime registry, resolver service, runtime coordination, provider behavior, branch/worktree behavior, target/apply behavior, release behavior, GitHub mutation, Gateway/network/model/provider calls, production readiness, or release readiness.

Stop at review. Do not implement EventRecord or any runtime surface in the check task.
