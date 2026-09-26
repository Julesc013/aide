# Stable interface contract rereview — c6d104f6

## Verdict

**ACCEPT_WITH_NOTES** — the superseding source/doc delta resolves both findings in the preserved `f0eabe41` REQUEST_CHANGES report. No blocking source or contract finding remains in this scope. One nonblocking receipt byte-normalization distinction is recorded below.

Acceptance is limited to predecessor feedback exclusion, helper API compatibility, narrowed partial-recovery wording and their focused evidence. It does not qualify full lifecycle suites, final archives, shipped support, activation, integration or publication. Permanent storage placement and full delivered-artifact qualification remain open.

## Frozen subject

- Candidate: `c6d104f665e3bc76ffd5c30ef600f66f014f50f3`
- Tree: `b05e73c554bef347fb6c3bffc0009ac83ccb1622`
- Parent: `f0eabe41265d9ff9a4388ccef4ef5c31c3e49854`
- Subject: `fix(import): protect predecessor packs from feedback output`
- Checkout reused read-only: `D:\Projects\AIDE\aide-stable-lite-partial-import-recovery`
- Prior report remains unchanged: `stable-interface-contract-review-f0eabe41.md`, SHA-256 `0c64a60dfbd53337e5232db2cce16b8f807e2c177b656fc791431e3b813abcd7`.
- No new checkout, fixture, probe, agent, bulk test, source/ref edit or tracked evidence write by the reviewer. Only this external report was created; no owned temporary fixture or live process remains.

## Prior finding disposition

### Predecessor-pack feedback exclusion — resolved

`write_import_feedback` adds an optional keyword-only `predecessor_pack: Path | None = None`. It resolves incoming pack and target roots, includes the resolved predecessor when supplied, and rejects a resolved output equal to or below any protected root before computing packet identity or creating the file. `command_import_pack` now passes its actual validated predecessor path into that helper. This closes the predecessor-local output admitted by the parent source.

The output parent is resolved before the exclusion test; the actual Windows-junction regression proves a path alias into the predecessor is refused. All normal supplied roots are normalized consistently. Existing exclusive `open("x")` creation, new-leaf/existing-parent validation, local packet shape and manual sharing behavior are retained.

Existing five-positional-argument helper callers remain valid and retain the default no-predecessor behavior. The new keyword is additive; existing CLI parser forms and import planning inputs are unchanged. The external/no-overwrite test explicitly exercises the original helper call and verifies real packet identity, manual-only sharing, no network flag, unchanged existing output bytes and refusal of a missing output directory.

### Partial versus completed/no-effect reconciliation wording — resolved

Policy now limits saved-full-plan/exact-original-input continuation to a **partially applied** import and limits the legacy snapshot refusal to **partial** intents. Reference documentation applies the same distinction. Both preserve separate completed/no-effect reconciliation or retirement behavior and clarify that those paths do not replay saved payload writes. That matches the existing source branch distinction described in the prior report, without changing recovery implementation or introducing an all-pending refusal promise.

The existing candidate gates still require final-manifest pinning of supported forms/options, metadata schemas, feature IDs, target states and evidence. Version is unselected and no shipping/activation authority follows from this repair. There is no optionality downgrade or automatic packet sharing.

## Test oracle adequacy

Three focused cases exercise the actual boundary:

1. Real CLI parsing and handler calls attempt feedback in each predecessor/incoming/target root, require refusal and absence of output, and verify original input files and file sets remain unchanged. They also exercise a successful external output. Only the expensive `apply_import_pack` plan is injected; real CLI forwarding, customization/explanation path, output guard, packet writer and identity are used.
2. Real helper backward compatibility and external packet creation, packet identity/manual-sharing/no-network flags, no overwrite, and refusal without creating a missing parent.
3. A real Windows junction into the predecessor, requiring refusal and no predecessor output; only the fixture junction itself is retired without traversing its target.

These tests do not simulate a full valid export/update pack or qualify lifecycle interactions. The unchanged checksum/planning behavior is intentionally outside this bounded regression. The narrow mock does not bypass the guard under review. Recorded zero skips establish that the Windows junction case actually ran.

The retained before-repair run provides a useful failing characterization: the real CLI admitted a predecessor-local feedback file and the input-state equality failed. Its junction case also errored because the old helper lacked the new keyword. That failure is preserved separately and is not mislabeled as a PASS.

## Verification and evidence

Reviewer commands/checks:

- `git show -s --format="%H %T %P%n%s" c6d104f665e3bc76ffd5c30ef600f66f014f50f3` — exact identity/subject above.
- `git diff --check f0eabe41265d9ff9a4388ccef4ef5c31c3e49854 c6d104f665e3bc76ffd5c30ef600f66f014f50f3` — PASS.
- Exact frozen source, tests, policy/reference and scoped task/driver delta review — both prior findings resolved.
- Independently hashed the final execution receipt's four declared code inputs against frozen Git blobs — all match the candidate, including Lite `c8e7b6307f95062ee59ff2de11715fb93d4517db4ed04cb2461c79a9fcc2a05d` and test module `46f5fce38c32c60a96e8b473417b8034072710218266be1aab6820fd90587d84`.
- Read frozen `feedback-boundary-before-repair.json` and `feedback-boundary-validation.json`; independently verified each retained raw log SHA-256 and size, then read the logs.
- Final log: **3 PASS in 0.082 seconds, zero skips**, exit 0 and quiescent. These are controller-executed results, not a duplicate reviewer test run.
- Compared the parser receipt's 28 rows with the frozen policy's 28 forms, verified all recorded PASS and code/policy hashes — PASS, no handler qualification claim.

Final raw log: `D:\Projects\AIDE\_recovery\resource-cleanup-20260926\bounded-feedback-boundary-check-4276e69ded414efdb56457f7b98cb1ab.log`

Raw-log SHA-256: `5c095d823657f699cd3723c87652b2a0c9cb16dd7a37270bf50e2d9ce60d8a4a`; 568 bytes.

The final bounded job used real unittest discovery selected by `-k feedback_boundary`; limits were 120 seconds, 8 MiB scratch, 512 MiB memory and 64 KiB logs. Recorded observed peaks were 708 scratch bytes and 212,582,400 Job memory bytes. Receipt reports retired/quiescent state and released reservation; actual recorded scratch absence was independently observed.

Execution receipt correctly retains precommit base HEAD/tree `f0eabe41265d9ff9a4388ccef4ef5c31c3e49854` / `2a6b1d9608851d1ab5e0fcd3a2503c2ceb7af6bc` alongside the changed code hashes. All four executed code hashes match this frozen candidate. This is code-byte-bound precommit evidence, not a clean candidate-HEAD run. The before-repair receipt and the final receipt remain distinct.

## Nonblocking evidence note

The review packet's nine binding rows require a byte-format distinction. Eight match their frozen Git blobs directly. For `candidate-cli-check.json`, recorded SHA-256 `e9420d1ce58b2adbe286a4c1ae5d8cb344ee964ac4c4b04e11d4165376abad6a` binds the Windows working file's CRLF bytes; the frozen Git LF blob has SHA-256 `c9ba2867efb21d645f387f6af4001b4db65e035fa61248808375aef5af222959`.

Reviewer confirmed both the working-file digest and that replacing every frozen LF with CRLF reproduces the recorded digest exactly. There is no JSON-content or code/policy binding discrepancy. The inner parser receipt still binds the correct candidate code/policy and exact 28 forms. Preserve both hashes and their byte subjects in evidence closeout; do not describe the working-byte hash as the frozen Git blob hash. This custody clarification does not require changing reviewed source or replacing the original receipt.

## Limits

No full export/import/archive/consumer suite or feedback handler fixture was independently executed by this reviewer. Path checks and the real junction test support the repaired supplied-root boundary; this review does not establish a hostile concurrent filesystem sandbox. Source acceptance is separate from full Windows delivered-byte support and final publication gates. Permanent bulk placement remains absent.

No further source repair is required for this exact scoped candidate.
