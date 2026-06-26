# DistributionManifest v1 Repair 01 Check

- result: REQUEST_CHANGES
- material_finding_count: 4
- missing_evidence: 0
- recommended_next_task: AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-02

## Material Findings

### protocol.future_major_not_implicitly_accepted

- source_finding_id: protocol.range_semantics_incomplete
- expected: distribution.unsupported_protocol_range unless explicit future-major support exists
- observed: `{"codes": [], "range": {"max": "2.x", "min": "1.0.0"}, "valid": true}`

### contamination.forbidden_path_classification_complete

- source_finding_id: contamination.forbidden_members_silently_filtered
- expected: observed forbidden reason for every independently forbidden path
- observed: `[{"expected": "forbidden_prefix", "observed": "forbidden_prefix:.aide.local/", "path": ".aide.local/state.sqlite"}, {"expected": "forbidden_exact", "observed": "forbidden_exact_member", "path": ".env"}, {"expected": "forbidden_exact", "observed": "forbidden_exact_member", "path": "raw-prompt.txt"}, {"expected": "forbidden_exact", "observed": "forbidden_exact_member", "path": "raw-response.txt"}, {"expected": "forbidden_prefix", "observed": "forbidden_prefix:.aide/context/latest-", "path": ".aide/context/latest-task-packet.md"}, {"expected": "forbidden_prefix", "observed": "forbidden_prefix:.aide/reports/", "path": ".aide/reports/distribution-manifest-v1/manifest.json"}, {"expected": "forbidden_prefix", "observed": "forbidden_prefix:.aide/repo/latest-", "path": ".aide/repo/latest-inventory.json"}, {"expected": "forbidden_prefix", "observed": "forbidden_prefix:.aide/roots/latest-", "path":`

### contamination.directory_forbidden_members_recorded

- source_finding_id: contamination.forbidden_members_silently_filtered
- expected: dirty and nested-dirty directories have forbidden members
- observed: `{"clean_forbidden": 0, "dirty_forbidden": 1, "nested_dirty_forbidden": 0}`

### fixture.future_major_protocol_fixture_present

- source_finding_id: fixture.required_coverage_incomplete
- expected: direct invalid future-major protocol fixture
- observed: `[]`

## Assertion Counts

- pass: 74
- fail: 4
- warning: 0
