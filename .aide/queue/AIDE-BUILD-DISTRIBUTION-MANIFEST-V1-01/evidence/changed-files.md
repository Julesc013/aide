# Changed Files

Primary implementation:

- `.aide/protocol/aide-distribution-manifest-v1.schema.json`
- `core/protocol/distribution_manifest.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_distribution_manifest_v1.py`

Generated/projection outputs:

- `.aide/reports/distribution-manifest-v1/**`
- `.aide/fixtures/distribution-manifest-v1/**`

Queue/planning records:

- `.aide/queue/AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

`git status --short --branch --untracked-files=all` was rechecked after broad
validation. All changed paths belong to this task's allowed path set.
