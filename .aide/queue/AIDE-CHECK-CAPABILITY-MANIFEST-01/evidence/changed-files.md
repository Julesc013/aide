# Changed Files

Intentional check-owned changes:

- `.aide/queue/AIDE-CHECK-CAPABILITY-MANIFEST-01/**`: check task packet,
  status, ExecPlan, prompt, and task-local evidence.
- `.aide/reports/capability-manifest-check/**`: aggregate check report,
  status report, and next-task prompt.
- `.aide/queue/index.yaml`: queue index entry for this check task.
- `PLANS.md`: plan index entry for this check gate.
- `IMPLEMENT.md`: execution log entry for this check gate.

Read-only checked paths:

- `.aide/queue/AIDE-BUILD-CAPABILITY-MANIFEST-01/**`
- `.aide/reports/capability-manifest/**`
- `.aide/protocol/aide-capability-manifest.schema.json`
- `core/protocol/capability_manifest.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_capability_manifest.py`

No CapabilityManifest implementation files were modified by this check.
