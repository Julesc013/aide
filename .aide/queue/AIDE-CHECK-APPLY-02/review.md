# AIDE-CHECK-APPLY-02 Review

## Decision

- disposition: NEEDS_REPAIR
- reviewed task: AIDE-APPLY-02-scoped-transaction-executor-v0
- implementation changed: false
- evidence basis: live queue packet, implementation commit `6a2f26985436394a92af22d3787381182dfa9dbc`, rerun validation, generated reports, static review, and AIDE-APPLY-02 evidence.

The implementation stayed inside the AIDE-APPLY-02 allowed paths and did not introduce install apply, upgrade apply, repair apply, rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.

The checkpoint is not accepted with notes because one required validation command failed, and static review found repair-worthy path-safety and apply-mode evidence gaps. The failures are bounded and do not show prohibited operation execution, so rejection is not warranted.

## Authorization Review

- AIDE-APPLY-02 task packet existed before implementation.
- AIDE-APPLY-02 had an ExecPlan, allowed paths, protected paths, forbidden operations, validation checklist, evidence requirements, and review gate.
- Implementation ended at `needs_review` / `implemented_needs_review`.
- Local commit `6a2f26985436394a92af22d3787381182dfa9dbc` contains the implementation.
- No push was performed during this checkpoint.

## Implementation Review

- executor entry point: `core/apply/transaction_executor.py`
- plan format: explicit JSON with `schema_version: aide.scoped-transaction-plan.v0`
- allowed operation types: `update_managed_section`, `report`, `validate`, `noop`
- path safety: lexical repo-relative normalization rejects absolute paths, traversal, wildcards, protected paths, and paths outside allowed roots, but does not resolve final target paths for symlink or reparse-point escape before read/write.
- managed-section integration: uses `core.apply.managed_sections` for canonical marker parsing and blocks missing, duplicate, malformed, nested, and ambiguous marker cases.
- preimage hash: computed with the managed-section SHA-256 helper before mutation and blocks mismatches.
- postimage verification: planned postimage expectations are checked; apply mode verifies post-write hash.
- rollback/staged-change records: generated and report-backed; rollback execution remains disabled.
- dry-run/report: dry-run and report modes produce evidence without target file mutation.
- failure behavior: preflight blockers fail closed; multi-operation apply still has partial mutation risk if a later write or post-write verification fails.

## Material Findings

1. Required example-plan validation fails.

   `py -3 .aide/scripts/aide_lite.py scoped-transaction run --plan .aide/examples/apply/scoped-transaction-executor.dry-run.example.json` exits 1 with `BLOCKED_PREIMAGE_HASH_MISMATCH`. The example file is structurally valid but uses placeholder `sha256:example-preimage` and `sha256:example-postimage` values, so it is not a passing runnable example.

2. Path safety is lexical and does not check resolved final targets.

   `validate_target_path` normalizes and compares path strings, then planning and apply use `self.repo_root / rel_path`. The executor does not resolve the final target and prove it remains under the repo root and allowed roots after symlink or reparse-point resolution before read/write.

3. Apply mode can leave partial target mutation after a late write or verification failure.

   `apply_staged_changes` writes staged changes sequentially. If multiple staged changes are present and a later write/read or postimage verification fails, earlier writes remain. The failure is reported, but v0 does not yet limit apply to one file, use atomic staging, or create an automatic restore path.

4. Core direct report output omits `report_path` in the persisted report.

   `write_available_outputs` writes the report JSON before assigning `report["report_path"]`. AIDE Lite fixture wrappers rewrite the generated report with the path present, but direct core execution with `write_outputs=True` can persist a report missing its own `report_path`.

## Non-Blocking Notes

- The CLI `scoped-transaction run --plan` resolves the plan path against the current process directory, not `--repo-root`. This is acceptable for the current repo-local workflow but should be clarified or tested if cross-cwd invocation is expected.
- The report schema is intentionally permissive with `additionalProperties: true`; this is acceptable for v0 but future review should tighten record requirements before wider apply use.

## What This Decision Does Not Authorize

This checkpoint does not authorize production-ready, release-ready, target-repo capable, install apply, upgrade apply, repair apply, rollback/uninstall apply, broad active-repo apply, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, or network calls.
