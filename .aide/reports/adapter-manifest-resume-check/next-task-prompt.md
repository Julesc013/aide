# AIDE-RESUME-ACCEPT-ADAPTER-MANIFEST-01

Create and process `AIDE-RESUME-ACCEPT-ADAPTER-MANIFEST-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Preserve the original
blocked `AIDE-ACCEPT-ADAPTER-MANIFEST-01` record as historical evidence; do not
rewrite or reuse it.

Review the original blocked AdapterManifest records, the resume build, and this
independent resume check. If no material findings remain, accept only the
minimal declaration-only `minimal_adapter_manifest_schema` capability.

Acceptance must not admit, trust, execute, launch, sandbox, resolve credentials,
call providers, call network services, mutate GitHub, create branches/worktrees,
apply patches, mutate target repositories, or implement runtime behavior.

Recommended next task after successful acceptance:

```text
AIDE-RESUME-BUILD-CONTEXTPACK-V2-01
```
