# ExecPlan: current partial-recovery projection

## Objective and source

Project accepted partial-recovery and resource-runner source already on
`dev@1d3d9fe1`. Runtime source `8040b10a` has independent
ACCEPT_WITH_NOTES and 110/110 importer methods passed in two bounded D jobs.
The following two commits only record task and evidence state; they do not
alter runtime source or test oracles. This task owns derived artifacts and
their delivered-byte qualification, not a new implementation.
The partial-recovery and resource WorkUnits remain open for this artifact
closure, so admission binds their accepted source/evidence slices instead of
waiting for their terminal task states.

## Plan

1. Admit this WorkUnit on a logical branch in the existing checkout, commit
   the queue record and verify clean source. Confirm current dev ancestry,
   D roots, canonical output volume identities and finite reservations.
2. Run the accepted `export-pack`, `changelog preview`, `release bundle`,
   `release validate`, `release draft` and `release draft-validate` commands
   serially through the D managed runner. Collect bounded receipts and hashes.
3. Run current `pack-status`, `doctor`, `validate`, release and provenance
   checks. Test extracted current ZIP/tar bytes in fresh and brownfield
   disposable consumers, including guarded partial recovery, customization,
   conflict preservation, repair, rollback, removal and promised offline use.
4. Commit exact generated outputs. Run the four release commands against
   clean committed HEAD and require zero changed files after bounded release
   metadata convergence. Validate pack source ancestry separately: `export-pack`
   intentionally writes current HEAD into its manifest and cannot be a
   zero-change generator after its own tracked output is committed.
5. Freeze exact source/tree, archives and evidence. Seek independent artifact
   and dev-effect review. Only after qualified GO, refresh refs and fast-forward
   dev with normal push and observed remote identity.

## Recovery and limits

One intensive job at a time. No new physical checkout or fallback pool.
Preserve source custody, required logs, failed attempts and canonical outputs.
Do not rerun unchanged source tests solely because this task adds queue records;
explain valid dependency/oracle bindings. Do not call preview bytes published
or stable. A defect in generator/source gets a separate bounded repair and
changed-scope review.

## Progress

- [x] Dev includes reviewed source; 110 importer methods passed in two D jobs.
- [x] Admit and commit the clean projection task at `84e4a733`.
- [x] Generate and qualify current bytes and consumers.
- [x] Prove committed four-command release replay with zero changes.
- [ ] Receive exact artifact/dev-effect review.
- [ ] Integrate qualified artifact candidate into dev.

Generation checkpoint: six serial D-managed commands exited zero, retired
scratch and released reservations. Current ZIP/tar hashes, provenance,
validation and exact job receipts are in `evidence/generation-84e4a733-20260928.md`.
Canonical check/inspect commands passed without rewriting source or unrelated
paths. Delivered consumers remain open.

Artifact commit `4b5854f2` froze initial ZIP/tar hashes. First clean-HEAD
replay passed all six commands but changed 30 tracked metadata/derived files;
zero-change replay therefore failed. Exact external job results and the
archive-member comparison are in task evidence. Only the archive manifest
member changed; payload members stayed byte-identical. Commit this bounded
metadata convergence. The second six-command replay from `dcb008e6` again
changed exactly 30 derived files because export always binds its manifest to
current HEAD. Those disposable regenerated changes were restored to the
committed tree after their receipts were retained. The committed four-command
release replay then exited zero but changed 18 release metadata files as the
pack was classified `PASS_SOURCE_ANCESTOR`; ZIP/tar bytes stayed unchanged.
Commit this 18-file convergence and require a clean four-command replay.

Convergence commit `49c7a04a` passed the clean four-command D-managed release
replay with zero changed files, unchanged ZIP/tar bytes and pack-status
`PASS_SOURCE_ANCESTOR`. Its exact job receipt and canonical checks are in
`evidence/delivered-qualification-49c7a04a.md`. An extracted ZIP/tar canary
passed 25 fresh/brownfield commands and explicit partial recovery after both
fresh import and successor update. Its one bounded D job retired scratch and
retained only 2.89 MB of command evidence. Exact artifact/effect review remains
the next gate before dev integration; this is not stable release acceptance.
