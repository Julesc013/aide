# Latest Golden Tasks

- result: PASS
- task_count: 10
- pass_count: 10
- warn_count: 0
- fail_count: 0
- provider_or_model_calls: none
- network_calls: none
- raw_prompt_storage: false
- raw_response_storage: false
- token_quality_statement: Token reduction remains valid only if golden tasks pass.

## Tasks

### adapter-managed-section-determinism

- result: PASS
- checks_run: 4
- passed_checks: 4
- approx_tokens_if_applicable: n/a
- related_paths: AGENTS.md
- notes: Checks managed section replacement on an isolated fixture repo.

### changelog_preview_golden

- result: PASS
- checks_run: 5
- passed_checks: 5
- approx_tokens_if_applicable: n/a
- related_paths: .aide/changelog/CHANGELOG.preview.md, .aide/changelog/RELEASE_NOTES.preview.md, .aide/policies/commit-messages.yaml
- notes: Checks deterministic changelog preview grouping and malformed commit reporting.

### commit_message_standard_golden

- result: PASS
- checks_run: 14
- passed_checks: 14
- approx_tokens_if_applicable: n/a
- related_paths: .aide/git/commit-template.md, .aide/hooks/commit-msg, .aide/policies/commit-messages.yaml, .aide/reports/aide-commit-message-standard.md
- notes: Checks changelog-ready commit message validation anchors.

### compact-task-packet-required-sections

- result: PASS
- checks_run: 17
- passed_checks: 17
- approx_tokens_if_applicable: 916
- related_paths: .aide/context/latest-task-packet.md, .aide/policies/token-budget.yaml, .aide/prompts/compact-task.md
- notes: Checks the compact task packet shape and forbidden prompt discipline.

### context-packet-no-full-repo-dump

- result: PASS
- checks_run: 17
- passed_checks: 17
- approx_tokens_if_applicable: 486
- related_paths: .aide/context/context-index.json, .aide/context/latest-context-packet.md, .aide/context/repo-map.json, .aide/context/test-map.json
- notes: Checks context refs instead of whole-repo dumps.

### review-packet-evidence-only

- result: PASS
- checks_run: 20
- passed_checks: 20
- approx_tokens_if_applicable: 2066
- related_paths: .aide/context/latest-review-packet.md, .aide/prompts/evidence-review.md, .aide/verification/review-packet.template.md
- notes: Checks review packet evidence-only shape.

### task_resumption_standard_golden

- result: PASS
- checks_run: 15
- passed_checks: 15
- approx_tokens_if_applicable: n/a
- related_paths: .aide/context/latest-task-packet.md, .aide/policies/task-resumption.yaml, .aide/queue/index.yaml, .aide/reports/aide-task-resumption-standard.md
- notes: Checks repeated and out-of-order task recovery policy anchors.

### token-ledger-budget-check

- result: PASS
- checks_run: 14
- passed_checks: 14
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/token-ledger.yaml, .aide/reports/token-ledger.jsonl, .aide/reports/token-savings-summary.md
- notes: Checks estimated token metadata without raw prompt or response storage.

### verifier-detects-bad-evidence

- result: PASS
- checks_run: 3
- passed_checks: 3
- approx_tokens_if_applicable: n/a
- related_paths: .aide/evals/golden-tasks/verifier-detects-bad-evidence/fixtures/missing-sections.md, .aide/verification/evidence-packet.template.md
- notes: Passes when the verifier refuses to accept malformed evidence silently.

### workunit_idempotency_golden

- result: PASS
- checks_run: 17
- passed_checks: 17
- approx_tokens_if_applicable: n/a
- related_paths: .aide/policies/recovery.yaml, .aide/policies/work-units.yaml, .aide/reports/aide-workunit-recovery-standard.md
- notes: Checks WorkUnit idempotency and no-op behavior.

## Limitations

- Deterministic local checks only.
- No model/provider/network calls.
- No external benchmark or arbitrary code semantic proof.
