# Validation

Validation result: PASS_WITH_WARNINGS.

## Capability Commands

- `py -3 .aide/scripts/aide_lite.py capability status`: PASS; seed_count=13; command_count=5.
- `py -3 .aide/scripts/aide_lite.py capability scan`: PASS; wrote observations JSON/Markdown; observation_count=47.
- `py -3 .aide/scripts/aide_lite.py capability ledger`: PASS; wrote ledger JSON/Markdown; record_count=13; state counts: planned=1, specified=3, stubbed=1, implemented=1, tested=1, exposed=1, documented=2, deprecated=1, removed=1, unknown=1.
- `py -3 .aide/scripts/aide_lite.py capability overclaim-report`: PASS; wrote overclaim JSON/Markdown; overclaim_count=1; blocking=false.
- `py -3 .aide/scripts/aide_lite.py capability validate`: PASS.

## Tests And Evals

- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS.
- `py -3 .aide/scripts/tests/test_x_os_02_capability_reality.py`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py eval run --task capability_seed_presence_golden`: PASS, 90/90 checks.
- `py -3 .aide/scripts/aide_lite.py eval run --task capability_command_surface_golden`: PASS, 10/10 checks.
- `py -3 .aide/scripts/aide_lite.py eval run --task capability_ledger_generation_golden`: PASS, 23/23 checks.
- `py -3 .aide/scripts/aide_lite.py eval run --task capability_overclaim_report_golden`: PASS, 8/8 checks.
- `py -3 .aide/scripts/aide_lite.py eval run --task capability_no_apply_boundary_golden`: PASS, 21/21 checks.
- `py -3 .aide/scripts/aide_lite.py eval run --task capability_export_pack_inclusion_golden`: PASS, 18/18 checks.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 158/158 golden tasks, 0 warnings, 0 failures.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_*.py"`: PASS, 325 tests in 645.352 seconds.

## Repo Validation

- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py export-pack`: PASS; included_files=743; checksum_count=746; boundary_result=PASS; provider/model calls none; network calls none.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums_valid=true; provenance_result=DIRTY_SOURCE_RECORDED; boundary_result=PASS.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS; checked_files=89; changed_files=83; warnings=0; errors=0.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS; wrote `.aide/context/latest-review-packet.md`; budget status PASS.
- `py -3 .aide/scripts/aide_lite.py pack --task "AIDE-CHECK-OS-01 - Task OS and Validation Telemetry Checkpoint: review X-OS-00, X-OS-01, and X-OS-02 evidence, warning disposition, validation telemetry, export-pack state, capability reality, and no-apply boundaries before any apply-capable Task OS phase."`: PASS; wrote `.aide/context/latest-task-packet.md`; budget status PASS; latest task packet now points to AIDE-CHECK-OS-01.
- `py -3 .aide/scripts/aide_lite.py route explain`: PASS as advisory route output; route_class=frontier; verifier_status=PASS; golden_task_status=PASS; provider/model calls none; network calls none. It reports token_budget_status=over_budget and quality_gate_status=WARN for advisory routing.
- `py -3 .aide/scripts/aide_lite.py git plan`: BLOCKED advisory helper plan; dry_run=true; apply_requested=false; push_requested=false; branch/remote mutation false; blocker is expected `dirty_tree_requires_classification` before the X-OS-02 commit.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; one warning: `.aide/generated/manifest.yaml` source fingerprint is stale.
- `git diff --check`: PASS.
- Targeted secret scan over X-OS-02 capability sources, queue packet, capability reports, docs, and test file: PASS, no matches for private-key or provider-token patterns.

## Warning Classification

- `expected_review_gate`: expected; X-OS-02 stops at `needs_review`.
- `expected_dirty_pack_provenance`: expected before the structured X-OS-02 commit; `pack-status` records `DIRTY_SOURCE_RECORDED` with zero checksum or boundary problems.
- `expected_generated_state`: root Harness v0 reports stale `.aide/generated/manifest.yaml`; this is an existing generated-manifest warning and not a capability blocker.
- `route_token_budget_advisory`: `route explain` reports token_budget_status=over_budget and quality_gate_status=WARN for routing advice; no provider/model/network calls were made.
- `git_helper_dirty_tree`: `git plan` is dry-run/report-only and records the expected dirty tree before the structured task commit; no branch, remote, or worktree mutation occurred.
- `nonblocking_overclaim_review`: capability overclaim report records one non-blocking wording review for `capability_reality_ledger` because report-only capability text mentions apply boundaries; result remains PASS.
