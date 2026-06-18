# Generated Output Ledger

- task_id: AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01
- result: PASS_WITH_WARNINGS
- repository_ref: fe877cc
- baseline_ref: AIDE-ACCEPT-DOC-KNOWLEDGE-TRUTH-RECONCILER-01
- ledger_path: .aide/ledgers/generated-output.yaml
- scanned_path_count: 1381
- classified_count: 1381
- unknown_count: 67
- finding_count: 9
- recommended_next_task: AIDE-BUILD-REPORT-INDEX-01
- independent_check_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

## Counts By Classification

- exported_copy: 818
- generated_context: 12
- generated_report: 470
- projection: 54
- tool_specific_projection: 24
- unknown_candidate: 3

## Counts By Severity

- info: 4
- warning: 5

## Findings

### GOL-001

- severity: info
- surface: generated_outputs
- taxonomy: truth_alignment_confirmed
- claim: Generated-output candidates were classified without applying repairs.
- expected: The ledger should observe and classify candidates without regenerating, deleting, or rewriting artifacts.
- observed: Classified 1381 candidate generated/projection/export/report artifacts.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### GOL-002

- severity: warning
- surface: generated_outputs
- taxonomy: generator_unknown
- claim: Some generated-output candidates have unknown generators.
- expected: Every generated or projected artifact should eventually have a known or explicitly inferred generator.
- observed: 67 candidates have unknown generator status.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### GOL-003

- severity: warning
- surface: generated_outputs
- taxonomy: freshness_unknown
- claim: Freshness is unknown for many generated-output candidates.
- expected: Freshness should remain unknown unless source fingerprints and generation rules prove otherwise.
- observed: 1381 candidates have unknown freshness.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### GOL-004

- severity: warning
- surface: generated_outputs
- taxonomy: consumer_unknown
- claim: Consumer references are not fully known for generated-output candidates.
- expected: Consumer discovery should be deterministic and explicit before delete or regeneration claims are made.
- observed: 1381 candidates retain consumer_unknown.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### GOL-005

- severity: warning
- surface: generated_report
- taxonomy: generated_truth_risk
- claim: Reports and projections can be mistaken for canonical truth if not explicitly bounded.
- expected: Generated reports, OKF projections, and context projections should default to non-canonical unless reviewed policy proves otherwise.
- observed: 514 candidates carry generated_truth_risk.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### GOL-006

- severity: warning
- surface: okf_knowledge
- taxonomy: missing_evidence
- claim: Some projection candidates lack source references.
- expected: Generated and projected artifacts should eventually identify source refs and source hashes where cheap and deterministic.
- observed: 1041 candidates have unknown source refs.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### GOL-007

- severity: info
- surface: context_projection
- taxonomy: truth_alignment_confirmed
- claim: Context projections are classified as non-canonical generated context.
- expected: Context packets and maps should remain projections, not queue or protocol truth.
- observed: 12 context projection candidates were classified.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### GOL-008

- severity: info
- surface: interop_projection
- taxonomy: truth_alignment_confirmed
- claim: Tool-specific projection roots are classified without making them canonical.
- expected: .agents and .codex surfaces should not become hidden AIDE queue or protocol truth.
- observed: 24 tool-specific projection candidates were classified.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

### GOL-009

- severity: info
- surface: export_projection
- taxonomy: truth_alignment_confirmed
- claim: Export pack artifacts are classified as exported copies.
- expected: Export pack copies should not become source-generated target truth for the live AIDE repo.
- observed: 818 export artifacts were classified.
- next_task: AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01

## Explicit Non-Capabilities

- automatic_regeneration
- automatic_deletion
- automatic_cleanup
- source_rewrite
- okf_regeneration
- report_migration
- reference_rewrite
- file_move
- file_rename
- migration_apply
- runtime
- provider_calls
- network_calls
- github_mutation
- branch_worktree_automation
- release_behavior
- target_repo_mutation
