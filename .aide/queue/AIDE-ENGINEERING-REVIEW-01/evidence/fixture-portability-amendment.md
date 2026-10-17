# Repair the demonstrated delivered self-test gap

This amendment extends the accepted engineering-review child under the standing
campaign delegation. It does not erase admission4dc6deb4 or the original failure.

Job46327979667a4d5ba2abf36ac40596a1 completed and retired: ownership6, exporter,
doctor, validation and pack-status PASS; exact858 members/five payload changes;
public1.0.0 unchanged. Delivered7 ran: six PASS, existing command/selftest method
FAIL at run_selftest's verifier assertion. Original logs/results are retained.
The refreshed export is preserved as an unqualified candidate, not discarded.

Read-only source tracing identifies two fixture portability defects:

- `_write_minimal_repo` correctly creates fallback `.gitignore`, then its Q18 loop
  replaces it with a generic placeholder when exported source lacks `.gitignore`.
  The unchanged verifier requires the local-state ignore rules.
- Export intentionally excludes source token baselines. The Q14 fallback writes
  no named baselines, but the unchanged self-test subsequently requires
  root_history_baseline and the summary uses review_baseline.

Extend allowed source scope only to `_write_minimal_repo` for these two cases and
the first verifier assertion's diagnostic message. Preserve its assertion and all
other semantic checks. Keep the initialized ignore file; provide small explicitly
synthetic fixture baseline definitions when the source record is absent. Do not
copy source reports into delivered projects, relax the verifier, skip assertions,
change actual project defaults or make broader self-test claims in advance.
Add one focused absence regression to existing test_review_pack.py.

Finite allocation amendment: maximum becomes four, with two consumed. Allocation3
is one new repair qualification, not a retry of unchanged inputs: original source
methods plus the absence regression, existing-owner refresh of changed CLI/tests,
and all original delivered methods plus regression. Use fresh separate processes
for source and delivered suites so the process-wide self-test cache cannot mask
different subjects. Source and delivered self-test assertions remain mandatory.
Require error diagnostics and preserve partial successes on failure. Reuse prior
prompt exercises unchanged. Allocation4 remains the existing promotion preview.
No further retry or broader repair follows automatically from this amendment.

Existing paths, limits, reserves, roots, exact input/effect review, evidence,
collection/retirement, public-asset preservation and Git gates remain unchanged.
Freeze the failed export in a structured checkpoint before observing its next
ownership inventory. Later source/effect review precedes the new qualification.
Do not integrate or publish while delivered acceptance remains failed.
