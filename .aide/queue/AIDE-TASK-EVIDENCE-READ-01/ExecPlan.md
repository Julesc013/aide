### Retained evidence in an ordinary task view

**Objective.** A completed task must not lose its evidence paths or recommend
record reconciliation merely because its ordinary qualification receipts exceed
the task YAML size budget. This is a concrete P0/P3 daily-use defect, observed
after actual browser qualification was integrated. The broad campaign remains open.

**Observed subject.** At bbc80a8c the browser task's source and preview receipts
are 266385 and 282661 bytes. Current task observation calls the 128-KiB record
reader, reports record_too_large with null paths and consequently recommends
reconcile_records. The files and passed task state remain intact. No retry,
new host probe, model call or prior evidence rewrite is needed.

**Existing owner and design.** Extend the task-view reader in aide_lite.py.
Keep task/status and all existing task_view_read caller limits unchanged.
Factor its ordinary safe-path validation once; use it for record reads and a
streaming evidence digest. Evidence reads are capped at 1 MiB per reference,
in at most 64-KiB chunks, with at most 16 references (16 MiB plus one
overflow-detection byte per reference). Reject metadata oversize before opening;
also detect growth past the limit during reading. Do not emit evidence bodies.
Preserve safe paths for oversized ordinary files. Unsafe/private/link paths
remain null. Missing, unreadable, invalid/mismatched digest and oversized states
remain distinct. Hash equality remains byte identity only; applicability stays
unverified and no execution or acceptance authority is added.

**Scope.** Change only existing reader, its current-task behavioral tests and
task-packet reference. No new status store, schema, command, frontend, global
read-limit change or Windows-only dependency. Existing path guards are not an
atomic snapshot or hostile-writer isolation. Product payload changes only the
CLI and existing test file; refresh existing export metadata through its owner.
Source-only reference documentation remains outside pack payload as applicable.

**Sequence.**
1. Independently review packet and local branch/admission commit effect.
2. Prepare exact source/tests/docs and one task-local runner. Independently
   review source and native job1. Preserve every existing current/handoff/binding/
   brief/HTML/symbol assertion. Add meaningful large receipt, boundary, streaming,
   changed digest, unsafe-link, bounded-growth and consumer continuation cases.
3. Job1 qualifies source and actual browser-task current/resume/brief observations.
   Compare unaffected small evidence with predecessor. Confirm large receipts now
   remain present, original result/limitations retained, no authority or mutation.
4. Refresh only existing capability source bindings if required, with exact review.
   Job2 uses owned pack refresh and safe disposable install. Run same delivered
   checks, six pack-ownership checks and an independently authored target fixture
   with >128-KiB evidence, customization and no core tree. Compare complete installed
   and source observations for the real task. Frozen eight release assets unchanged.
5. Job3 uses existing fixed-range changelog preview and retained evidence verification.
   Finish concise root/parent/status records, exact independent integration review,
   safe dev/main synchronization and retirement of only this local task branch.

**Resource boundary.** Three finite native allocations using unchanged existing
config, roots, shared controls and per-job 180sec/1GiB/16process/32MiB scratch/
8MiB retained caps and reserves. Every launch needs fresh exact admission.
Collect and retire on success or failure; no automatic retries or cap changes.
No provider/model/network/browser/target/desktop/auth/storage-layout effects.
Pack and preview canonical writes require their separately reviewed manifests.

**Acceptance.** Existing small-record safety and output behavior remain covered.
Legitimate large evidence supports inspect_completed_evidence for completed work
while obligations and non-authority fields remain. Oversized and malicious inputs
still refuse with useful safe metadata. New tests reject the old size behavior.
Source, delivered, installed and real-source checks identify exact subjects.
No whole-task efficiency or additional host support is inferred.

**Recovery.** Preserve all original failures and receipts. An interrupted effect
is reconciled through existing owners before another attempt. No evidence deletion,
history rewrite or blind replay. Stop on changed inputs, unresolved review,
resources, unexpected payload changes or failed qualification. Independent work
may continue when another route remains blocked.

**Progress.** Packet prepared; no implementation or execution authorized by this
draft. Prior turn completed browser qualification and dev/main integration.

**Progress update.** Independent admission accepted the exact nine-file map.
Admission committed at51ce6c7b; source preparation is in progress.

**Source observed.** Source checkpoint 347668a4 passed all168 methods, actual
large-evidence paths/continuation and complete HTML/JSON equality. Small-evidence text/JSON match the predecessor; actual large receipts are now readable.
Jobcb8f978da79f4746bfcdbf0e8285cb4c retired quiescent; all collection digests
verified, scratch absent and reservation released. Original structural FAIL stays.
Only the existing four-output capability binding refresh is now proposed.

**Delivery prepared.** Reviewed existing capability refresh kept classifications
unchanged and made source binding CURRENT. The second allocation targets the
same875 pack members, delivered168 and an independent installed large-evidence
fixture. Actual source/installed observations must agree completely. This
preparation does not establish delivered qualification.
