# Reconciler Finding Taxonomy

- task_id: AIDE-BUILD-RECONCILER-REPORTS-01
- report_only: true
- repair_authorized: false

## Categories

- stale_context: severity=warning; Generated context packets lag the canonical filesystem queue.
- acceptance_gate_debt: severity=warning; Queue items remain implemented or accepted but still parked at needs_review review gates.
- queue_contradiction: severity=warning; Queue records disagree with their task-local records or review state.
- missing_evidence: severity=error; A queue or report record references evidence that is absent from the filesystem.
- missing_report: severity=error; A queue or protocol record references a required report that is absent.
- stale_generated_report: severity=warning; Generated reports reflect an older task routing state than the accepted queue chain.
- source_hash_gap: severity=warning; A generated knowledge page records a source hash that no longer matches the source file.
- protocol_report_mismatch: severity=warning; Protocol projection or validation reports disagree with their accepted protocol chain.
- protocol_okf_mismatch: severity=warning; OKF knowledge explains protocol state differently from protocol or queue reports.
- reference_mismatch: severity=warning; ReferenceID reports, locators, or OKF refs disagree.
- event_mismatch: severity=warning; EventRecord reports, event refs, or OKF event refs disagree.
- capability_overclaim: severity=error; A report or knowledge page claims an unimplemented capability.
- unsupported_accepted_state: severity=error; A record marks capability acceptance without the required reviewed predecessor evidence.
- authority_boundary_risk: severity=warning; A generated artifact could be mistaken for source truth if its boundary is not explicit.
- dirty_state: severity=warning; The repository state or generated report set changed during reconciliation.
