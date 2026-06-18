# Doc/Knowledge Truth Reconciler

- task_id: AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01
- result: PASS_WITH_WARNINGS
- scan_mode: full
- repository_ref: 54f7b2e
- baseline_ref: AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01
- source_count: 900
- finding_count: 12
- report_only: true
- mutation_performed: false
- recommended_next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

## Truth Precedence

1. accepted governance and policy
2. canonical protocol/schema definitions
3. .aide/queue/index.yaml and queue task status
4. build/check/accept evidence
5. accepted capability/conformance records
6. generated reports and indexes
7. OKF knowledge projections
8. human-facing documentation
9. generated context/tool-specific projections

## Counts By Severity

- info: 3
- warning: 9

## Counts By Surface

- acceptance_state: 1
- context_projection: 1
- documentation: 4
- evidence: 1
- okf_knowledge: 3
- policy: 1
- queue_state: 1

## Counts By Taxonomy

- projection_drift: 3
- reference_break_risk: 1
- stale_claim: 4
- status_mismatch: 1
- truth_alignment_confirmed: 3

## Findings

### DKT-001

- severity: info
- surface: acceptance_state
- taxonomy: truth_alignment_confirmed
- claim: Accepted self-management charter routes Track B to the doc/knowledge truth reconciler.
- expected: `AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01` recommends `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`.
- observed: accepted report recommended_next_task is `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`.
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

### DKT-002

- severity: info
- surface: queue_state
- taxonomy: truth_alignment_confirmed
- claim: The current build task is registered in the canonical queue index.
- expected: `.aide/queue/index.yaml` includes `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`.
- observed: `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01` is present in queue index.
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

### DKT-003

- severity: warning
- surface: policy
- taxonomy: status_mismatch
- claim: The original self-management policy sequence still routes RootAuthorityManifest before the doc/knowledge truth reconciler.
- expected: Accepted predecessor routing should be reflected or explicitly superseded by future policy/docs updates.
- observed: Policy required_sequence lists AIDE-BUILD-ROOT-AUTHORITY-MANIFEST-01 before AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01, while the accepted charter acceptance routes this reconciler next.
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

### DKT-004

- severity: warning
- surface: documentation
- taxonomy: stale_claim
- claim: The self-management reference still documents the earlier initial queue sequence.
- expected: Human docs should either match accepted next-task routing or explicitly mark older sequence text as superseded.
- observed: `docs/reference/aide-self-management.md` lists RootAuthorityManifest before DocKnowledgeTruthReconciler, while acceptance routes DocKnowledgeTruthReconciler next.
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

### DKT-005

- severity: warning
- surface: context_projection
- taxonomy: projection_drift
- claim: The latest generated task packet is stale relative to accepted Track B routing.
- expected: Generated context should mention `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01` after accepted routing, or remain clearly non-canonical.
- observed: Latest task packet phase is `AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01 - Check AIDE Self-Management Charter` and does not mention `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`.
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

### DKT-006

- severity: warning
- surface: okf_knowledge
- taxonomy: stale_claim
- claim: OKF next-work projection is stale relative to accepted Track B routing.
- expected: OKF next-work should explain `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01` or clearly indicate it predates the accepted charter acceptance.
- observed: OKF next-work still recommends AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01 and says not to recommend Reconciler directly from that older build slice.
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

### DKT-007

- severity: warning
- surface: okf_knowledge
- taxonomy: projection_drift
- claim: OKF queue current-state projection still describes the older OKF build slice.
- expected: OKF current-state pages should not be mistaken for current queue truth when their source hash or task text is stale.
- observed: OKF queue page names AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01 as the current slice.
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

### DKT-008

- severity: warning
- surface: okf_knowledge
- taxonomy: projection_drift
- claim: Some OKF pages record source hashes that no longer match their source files.
- expected: OKF source hashes should match the current source file when the projection is fresh.
- observed: .aide/knowledge/okf/current-state/next-work.md -> .aide/queue/index.yaml; .aide/knowledge/okf/current-state/queue.md -> .aide/queue/index.yaml; .aide/knowledge/okf/current-state/review-gates.md -> .aide/queue/index.yaml; .aide/knowledge/okf/current-state/stale-latest-task-packet.md -> .aide/queue/index.yaml; .aide/knowledge/okf/decisions/okf-as-knowledge-plane.md -> .aide/queue/index.yaml; .aide/knowledge/okf/decisions/protocol-vs-knowledge.md -> .aide/queue/index.yaml; .aide/knowledge/okf/decisions/repo-contract-vs-runtime-state.md -> .aide/queue/index.yaml; .aide/knowledge/okf/risks/acceptance-gate-debt.md -> .aide/queue/index.yaml; plus 2 more
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

### DKT-009

- severity: warning
- surface: documentation
- taxonomy: stale_claim
- claim: README implementation status still describes Reconciler reports as planned.
- expected: Human documentation should reflect that minimal Reconciler reports were accepted with warnings, while runtime repair remains deferred.
- observed: README table says `Reconciler reports | Planned`; queue status says AIDE-ACCEPT-RECONCILER-REPORTS-01 result ACCEPTED_WITH_WARNINGS.
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

### DKT-010

- severity: warning
- surface: documentation
- taxonomy: stale_claim
- claim: DOCUMENTATION current status groups Reconciler and CapabilityManifest with future phases.
- expected: Documentation should distinguish accepted report-only Reconciler, built/checked CapabilityManifest, and truly future Track A objects.
- observed: DOCUMENTATION.md still says Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, and ContextPack v2 remain future phases.
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

### DKT-011

- severity: warning
- surface: documentation
- taxonomy: reference_break_risk
- claim: Some inspected documentation or reports reference paths that are absent from the current worktree.
- expected: Path references used as evidence or documentation links should resolve, be glob placeholders, or be explicitly marked as examples.
- observed: .aide/queue/AIDE-ACCEPT-RECONCILER-REPORTS-01/evidence/check-model-review.md -> core/control/reconciler_reports.py; .aide/reports/contract-envelope-check/check-report.md -> core/protocol/envelope.py::validate_envelope
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

### DKT-012

- severity: info
- surface: evidence
- taxonomy: truth_alignment_confirmed
- claim: Selected acceptance/check status evidence references resolve.
- expected: Evidence refs in selected status files exist.
- observed: No missing evidence refs found for accepted self-management charter or CapabilityManifest check status.
- next_task: AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

## Explicit Non-Capabilities

- automatic_doc_repair
- automatic_okf_regeneration
- automatic_queue_repair
- automatic_evidence_repair
- file_moves
- file_renames
- reference_rewrites
- migration_apply
- generated_output_ledger
- runtime
- provider_calls
- network_calls
- github_mutation
- branch_worktree_automation
- release_behavior
- target_repo_mutation
