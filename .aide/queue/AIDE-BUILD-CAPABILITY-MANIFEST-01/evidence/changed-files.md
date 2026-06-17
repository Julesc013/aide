# Changed Files

Intentional task-owned changes:

- `.aide/protocol/aide-capability-manifest.schema.json`: CapabilityManifest schema.
- `core/protocol/capability_manifest.py`: deterministic declaration/projection/validation helper.
- `core/protocol/__init__.py`: protocol package export.
- `.aide/scripts/aide_lite.py`: thin `capability-manifest` CLI dispatch.
- `.aide/scripts/tests/test_aide_capability_manifest.py`: focused tests.
- `.aide/reports/capability-manifest/**`: generated CapabilityManifest reports.
- `.aide/queue/AIDE-BUILD-CAPABILITY-MANIFEST-01/**`: queue task, status, ExecPlan, prompt, and evidence.
- `.aide/queue/index.yaml`: queue index entry.
- `PLANS.md`: plan index entry.
- `IMPLEMENT.md`: implementation log entry.

Preflight-generated churn outside the deliverable was restored before
implementation.
