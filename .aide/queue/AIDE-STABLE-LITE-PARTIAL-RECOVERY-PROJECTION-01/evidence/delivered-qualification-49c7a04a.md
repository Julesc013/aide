# Committed Lite preview qualification, 2026-09-28

Clean candidate `49c7a04a13778c6da01e46c4cfffb8bfd0d0dcd3`, tree
`6fe51e8409616ac7dc59753679256d47f70f456b`, descends from
`dev@1d3d9fe1`. The portable pack declares clean source `4b5854f2`;
`pack-status` returned `PASS_SOURCE_ANCESTOR`, valid checksums and boundary,
zero problems. No portable input changed along that ancestry.

The four release commands (`bundle`, `validate`, `draft`, `draft-validate`)
ran serially through the D managed runner. All child/runner exits were zero,
scratch retired and reservations released. External results:
`D:\Projects\AIDE\.aide.local\execution\control\release-replay2-49c7a04a-results.jsonl`,
SHA-256 `3cff2266dd00506df414b9563d37edc4195c8cb6e9b1305434c58be57a1c2df3`.
After replay, both tracked and untracked change counts were **zero**. The
release validation reports PASS with 20 checks, zero blockers/warnings; draft
validation reports PASS with zero blockers/warnings. The ZIP and tar remained:

- ZIP SHA-256 `af8bf103353d72eacbbf1f2f28cea8cef1f11ea0d942872c57f76aee9725a7ff`.
- tar.gz SHA-256 `f0111bd834eb1aeb0b5b0ea70562ad7e1294c04dea8fa0bd83ab9be5cb294725`.

An offline delivered-byte canary consumed those exact archives in one D
managed job `1f8d550ffbac4809bc3052f42320884e`. Manifest SHA-256
`9acfa7a3b61c96663193e847e83be4f0814fb25e3abd183fc78a8888cfe4faf2`;
retained job receipt SHA-256
`b39f809360c63cc03b60d0faa27702048a34bf85b32848b5de6a301d4d20bb69`.
The pinned prior 25-command canary and a small local wrapper were bound as
hashed job inputs. The ZIP/tar had 834 matching safe members and a matching
reviewed source CLI digest. The 25 fresh/brownfield command oracles passed
(20 exit 0, five expected refusal exit 2), including direct edits, synthetic
successive updates/conflicts, disabled-feature preservation, repair health and
no feedback by default. Synthetic V2/V3 packs are disposable fixtures, not
published releases. Retained `summary.json` SHA-256
`40a87250481460974a2fa807e61d77ae2b5754cf31f8cfff76d0c5f39436c048`.

The same extracted delivered module proved fresh import and predecessor update
each followed `INTERRUPTED` → `RECOVERY_REQUIRED` → explicit `RECOVERED`.
Project-owned bytes were preserved and active intent retired. Retained
`partial-recovery-result.json` SHA-256
`9239bd512b9b73cfcc9d32a2cabe874cbc8997342dd89cd3cef05f0a19f70554`.
The job exited zero, peaked at 298,713,088 memory bytes and 33,258,088
scratch bytes, retained 27 evidence files totalling 2,891,866 bytes, retired
scratch and released its reservation. It wrote no canonical source outputs.

Canonical `doctor`, `validate`, `release status` and `release draft-status`
all exited zero and left the worktree clean. Their respective external log
SHA-256 values under D control are
`1135890d41d10a4d546978ab7b8e7b5992d80f1931cf4b21e6da6e411ed5ea21`,
`7b326b01165e7743abe7d770bad1646dab78f4a411352dfbd8faae83b383e789`,
`b025ed2cb65847c94c82019c1086271aa822522c78d03bee0f64903d15203651`,
and `c93a2fce5394fb06314eab9a1134644bf5cb239285df2823f7df162a92222a5`.
Commit range `1d3d9fe1..49c7a04a` passed four structured messages; an
evidence-only commit requires a fresh final range check and four-command
replay. Independent artifact/dev-effect review is pending. Main, tag,
publication, native/hosted and downloaded-byte acceptance are outside this
candidate decision.
