# Directory Contamination Report

- schema_version: aide.distribution-manifest-v1-repair-02.directory-contamination.v1
- source_member_count: 5
- allowed_members: ['files/src/allowed.py']
- forbidden_members: [{'path': 'files/.aide/context/latest-context-packet.md', 'reason': 'forbidden_prefix:.aide/context/latest-', 'source_member': 'files/.aide/context/latest-context-packet.md', 'target_member': '.aide/context/latest-context-packet.md', 'packaging_prefix': 'files', 'refusal_code': 'distribution.forbidden_member'}, {'path': 'files/.aide/reports/report.json', 'reason': 'forbidden_prefix:.aide/reports/', 'source_member': 'files/.aide/reports/report.json', 'target_member': '.aide/reports/report.json', 'packaging_prefix': 'files', 'refusal_code': 'distribution.forbidden_member'}, {'path': 'files/.aide.local/state.sqlite', 'reason': 'forbidden_prefix:.aide.local/', 'source_member': 'files/.aide.local/state.sqlite', 'target_member': '.aide.local/state.sqlite', 'packaging_prefix': 'files', 'refusal_code': 'distribution.forbidden_member'}, {'path': 'files/.env', 'reason': 'forbidden_exact_member', 'source_member': 'files/.env', 'target_member': '.env', 'packaging_prefix': 'files', 'refusal_code': 'distribution.forbidden_member'}]
- source_state_contamination_detected: True
- artifact_forbidden_member_count: 4
- validation_refusal_codes: ['distribution.source_state_contamination']
- passed: True
