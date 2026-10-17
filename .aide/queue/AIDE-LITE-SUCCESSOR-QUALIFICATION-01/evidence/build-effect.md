# Allocation 1: actual candidate build

Review the exact source map and build-job-template.json. Only source_commit/tree
placeholders may be replaced after the unchanged preparation commit. Use the
unchanged default .aide.local/execution.json, canonical digest
61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90.
Reserve existing .aide/release at8MiB;49 current members total4,030,243 bytes.
Only the four new1.1.0 outputs may change. Existing release and pack members are
immutable job inputs and checked before/after by run_build.py. Whole-parent
reservation includes them for ownership, not write authorization. No tag/upload.

Fresh exact source, clean task branch, all input/executable/config hashes, sole
checkout, pause and no shared active reservation before dispatch. Existing runner
performs fresh authoritative resource admission. Save original job result before
asserting success; verify collected output/log hashes, quiescence, scratch absence
and reservation release. Failure consumes allocation1 and stops. Do not retry.
CLI stable-build and stable-validate use existing owners with full raw streams.
Builder preserves source-pack lineage rather than pretending evidence-only HEAD
is a rebuilt payload. A passing build does not qualify consumers or publication.

Also review proposed consumer-config.json for later materialization at exact
.aide.local/lite-successor-qualification-execution.json. Only four task-scoped
limits change as admitted; no consumer is dispatched by this build effect.
The default config remains read-only. All roots, volume identities and reserves
stay exact. Config materialization follows ACCEPT; consumers need separate effects.

Prior source60/delivered25 results remain valid for unchanged code and pack.
Doctor passed. Initial full validation found stale capability evidence after new
queue registration; retain its failure, refresh through existing ledger owner,
and rerun. Existing global review-packet warning remains, with explicit rubric
references supplied in this child's dev-review-packet.md.

Rebound full validation PASS (exit0); sole warning remains the classified global review reference. Wrapper syntax and current input identities pass.
