# Directory Contamination Review

- schema_version: aide.check.directory-contamination-review.v1
- forbidden_members: [{'path': 'files/.aide/context/latest-context-packet.md', 'reason': 'forbidden_prefix:.aide/context/latest-', 'source_member': 'files/.aide/context/latest-context-packet.md', 'target_member': '.aide/context/latest-context-packet.md', 'packaging_prefix': 'files', 'refusal_code': 'distribution.forbidden_member'}, {'path': 'files/.aide/reports/report.json', 'reason': 'forbidden_prefix:.aide/reports/', 'source_member': 'files/.aide/reports/report.json', 'target_member': '.aide/reports/report.json', 'packaging_prefix': 'files', 'refusal_code': 'distribution.forbidden_member'}, {'path': 'files/.aide.local/state.sqlite', 'reason': 'forbidden_prefix:.aide.local/', 'source_member': 'files/.aide.local/state.sqlite', 'target_member': '.aide.local/state.sqlite', 'packaging_prefix': 'files', 'refusal_code': 'distribution.forbidden_member'}, {'path': 'files/.env', 'reason': 'forbidden_exact_member', 'source_member': 'files/.env', 'target_member': '.env', 'packaging_prefix': 'files', 'refusal_code': 'distribution.forbidden_member'}]
- allowed_members: ['files/src/allowed.py']
- source_state_contamination_detected: True
- validation_refusal_codes: ['distribution.source_state_contamination']
- recorded_detail_fields: ['packaging_prefix', 'path', 'reason', 'refusal_code', 'source_member', 'target_member']
- passed: True
