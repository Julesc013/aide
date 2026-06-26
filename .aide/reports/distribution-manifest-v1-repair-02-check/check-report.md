# DistributionManifest v1 Repair 02 Check Report

- schema_version: aide.distribution-manifest-v1-repair-02-check.report.v1
- task_id: AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-02
- source_task: AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-02
- source_commit: 24753ef84fed5613f8a276ef7bfb4ddd58d6d7d3
- result: PASS_WITH_WARNINGS
- material_finding_count: 0
- missing_evidence: 0
- recommended_next_task: AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01
- checks: {'protocol_range': True, 'contamination': True, 'directory_contamination': True, 'fixture_coverage': True, 'regression': True}
- warnings: ['DistributionManifest v1 remains unaccepted in this check task.', 'ProjectLock v0 was not started.']
