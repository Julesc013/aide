# Report Index

- task_id: AIDE-BUILD-REPORT-INDEX-01
- result: PASS_WITH_WARNINGS
- repository_ref: af3156a
- baseline_ref: AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01
- index_path: .aide/reports/index.yaml
- scanned_report_count: 479
- indexed_report_count: 479
- ambiguous_count: 70
- finding_count: 8
- recommended_next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01
- independent_report_index_check: AIDE-CHECK-REPORT-INDEX-01

## GeneratedOutputLedger Input

- status: present_provisional_unaccepted
- accepted: False

## Counts By Stage

- accept: 203
- audit: 6
- build: 19
- check: 62
- harden: 1
- reconciliation: 4
- repair: 61
- status: 55
- unknown: 68

## Counts By Severity

- info: 3
- warning: 5

## Findings

### RPT-001

- severity: info
- surface: generated_report
- taxonomy: truth_alignment_confirmed
- claim: Reports were indexed without moving or rewriting them.
- expected: Report indexing should observe tracked reports and leave historic report paths untouched.
- observed: Indexed 479 tracked report files.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### RPT-002

- severity: info
- surface: generated_report
- taxonomy: report_subject_ambiguous
- claim: Some report subjects are ambiguous.
- expected: Report subjects should be inferable from path, task id, or report metadata where practical.
- observed: 0 sampled ambiguous subject paths; full count is recorded in report records.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### RPT-003

- severity: warning
- surface: generated_report
- taxonomy: report_stage_ambiguous
- claim: Some report lifecycle stages are ambiguous.
- expected: Build/check/accept/status/inventory stages should be inferred only when evidence is sufficient.
- observed: 68 reports have unknown stage.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### RPT-004

- severity: warning
- surface: generated_report
- taxonomy: report_producer_unknown
- claim: Some report producers are unknown.
- expected: Producer should be known or inferred without inventing task authority.
- observed: 2 reports have unknown producer.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### RPT-005

- severity: warning
- surface: generated_report
- taxonomy: generated_truth_risk
- claim: Reports are generated discovery projections and not canonical truth.
- expected: Reports should default to canonical false unless accepted policy proves otherwise.
- observed: 479 indexed reports default to canonical false and generated true.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### RPT-006

- severity: warning
- surface: evidence
- taxonomy: missing_evidence
- claim: Some task-linked reports have missing evidence directories.
- expected: When a report names a task id, evidence should exist or absence should remain warning-class.
- observed: 23 reports reference task ids without discovered evidence directories.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### RPT-007

- severity: warning
- surface: generated_report
- taxonomy: reference_break_risk
- claim: Some task-linked reports have reference break risk.
- expected: Task status refs inferred by reports should resolve or remain warning-class.
- observed: 23 reports have task status reference risk.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### RPT-008

- severity: info
- surface: generated_report
- taxonomy: truth_alignment_confirmed
- claim: GeneratedOutputLedger input is treated as provisional.
- expected: ReportIndex may consume GeneratedOutputLedger build output only as unaccepted provisional information.
- observed: GeneratedOutputLedger build output is present and recorded as provisional_unaccepted.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

## Explicit Non-Capabilities

- report_move
- report_rename
- report_rewrite
- report_repair
- report_delete
- evidence_rewrite
- normalization
- migration_apply
- canonical_truth_replacement
- runtime
- provider_calls
- network_calls
- github_mutation
- branch_worktree_automation
- release_behavior
- target_repo_mutation
