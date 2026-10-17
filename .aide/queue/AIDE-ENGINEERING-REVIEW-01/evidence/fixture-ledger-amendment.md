# Generate self-test ledger from its actual fixture

Allocation3 job781d77883c594dd9a246923c6f5d0df1 at ca7bd44a ran eight source
methods PASS; ownership6/export/doctor/validate/pack-status PASS; delivered8
ran seven PASS and the original command/selftest failed the unchanged golden
assertion for token-ledger-budget-check. Collection and retirement are verified;
all exported bytes still equal the collected post-export inventory. Prior
failures and source successes remain preserved separately.

Static trace: run_selftest merges only a task_packet record. The golden requires
context_packet, review_packet and verification_report too. Source fixtures copied
historical token-ledger.jsonl and accidentally supplied those records; portable
fixtures correctly lack that source-only ledger. This is a fixture dependency,
not evidence that token-budget enforcement should be weakened.

Proposed bounded extension under the existing campaign delegation:
- Initialize only the disposable fixture TOKEN_LEDGER_PATH to empty, even if the
  source has a ledger. Preserve source records and all real project behavior.
- In run_selftest, use existing build_ledger_scan_records and merge owner to
  measure the generated fixture artifacts before the existing golden assertion.
  Preserve the explicit task record checks, every golden requirement and all
  other original assertions. Add failing check diagnostics to the same assertion.
- Extend the existing absence regression to include absent source ledger and
  exercise the actual ledger scan command plus unchanged token-ledger golden.
  Verify the empty fixture cannot pass the golden before measurement.
- Inspect the remaining self-test path for other source-report dependencies.

Maximum managed allocations becomes five, with three consumed. Allocation4 is
one corrected source/export/delivered qualification using separate fresh processes;
allocation5 is the unchanged promotion preview. No repeated unchanged attempt,
no more exercise reviewers, no new infrastructure or provider/target effects.
Preserve current failed-export bytes in a structured checkpoint before its next
inventory. All current reserves, limits, roots, original methods, export ownership,
public1.0.0 preservation and exact source/effect independent review still apply.
Another failure requires retained diagnosis; no further attempt is authorized by
this amendment. Do not promote until all original delivered assertions pass.
