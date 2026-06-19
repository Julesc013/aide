# AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01

Create and process `AIDE-RESUME-BUILD-ADAPTER-MANIFEST-01`.

Use `.aide/queue/index.yaml` as canonical queue truth. Preserve the original
blocked `AIDE-BUILD-ADAPTER-MANIFEST-01` task as historical evidence; do not
rewrite or reuse it.

Build the minimal AdapterManifest schema slice now that repaired
PatchTransaction acceptance has resumed. The slice defines declaration and
inspection of adapter integration shape only. It must not admit, trust,
execute, launch, schedule, sandbox, call providers, call network services,
mutate GitHub, create branches/worktrees, apply patches, mutate target
repositories, or build runtime behavior.

Recommended next task after a successful build:

```text
AIDE-RESUME-CHECK-ADAPTER-MANIFEST-01
```
