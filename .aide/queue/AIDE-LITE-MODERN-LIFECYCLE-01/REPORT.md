### Modern lifecycle observations

**Outcome:** real delivered adoption and project-content preservation succeeded on four exact environments. Removal succeeded on the two Windows profiles and refused on Linux/macOS because the existing implementation requires Windows anchored handles. This characterization is complete; **Lite 1.2 and Linux/macOS lifecycle support remain unqualified**.

| Observed environment | Fixture suite | Adoption and preservation | Removal |
|---|---|---|---|
| Windows 10 build 19045, x64, CPython 3.14.8 | 117 pass, 9 environment skips | Four cases passed | Four passed |
| Windows Server 2025 build 26100, x64, CPython 3.14.8 | 124 pass, 2 environment skips | Four cases passed | Four passed |
| Ubuntu 24.04 runner, kernel 6.17.0-1022-azure, x64, CPython 3.14.8 | 125 pass, Windows-only case skipped | Four cases passed | Four original refusals retained |
| macOS 15 runner, Darwin 24.6.0, arm64, CPython 3.14.8 | 125 pass, Windows-only case skipped | Four cases passed | Four original refusals retained |

Each environment exercised published **1.1.0** and the unchanged **development export**, with both fresh and existing-project targets. Brownfield cases preserved authored guidance, a newly appended manual rule, plans, history, memory and an existing tool. Native lifecycle acceptance is a separate field from observation completion. The development export is a prior validated snapshot, not a 1.2 release candidate.

**Evidence:** [local retirement and qualification](evidence/local-qualified.json), [full local result](evidence/local-result.json), [hosted observations](evidence/hosted-observed.json), [actual refusal classification](evidence/native-gap-classification.json). [GitHub run 39403629036](https://github.com/Julesc013/aide/actions/runs/39403629036), attempt 1, used immutable source `f4d099a2b5fd29da83a1a1be1e7f9026e17e4f6e`; all three observation jobs completed. Exact runner images, Python executables and source identities are retained. Job success does not turn refused removal into a pass.

**Resource and recovery:** one local allocation exited zero, collected and hash-verified its evidence, removed owned scratch and released reservations. Observed peaks were 283,324,416 bytes of worker memory and 16,066,428 bytes of scratch. All 67 local receipt files round-tripped byte for byte. One hosted workflow ran three standard public jobs with ten-minute bounds, no artifact/cache upload and no model calls. The collector enforced its remaining deadline and byte caps, collected attempt-specific logs and checked final run identity. Controller/reviewer usage remains unknown.

**Review:** independent reviews first rejected durability/preservation/helper-gate gaps and then hosted bounds/attempt gaps. Their original verdicts, manifests and changed source bytes remain. The repaired source/local effect and hosted effect separately received actual ACCEPT. Final outcome/source and dev/main integration still require their exact review and transaction receipt; no public product or tag changes are included.

**Next implementation:** extend the existing lifecycle owner with a small POSIX filesystem binding for verified directory/file identity, no-follow access, no-clobber publication, ownership-safe removal and recoverable updates. Reuse lifecycle plans, receipts, conflicts and recovery semantics. Keep Windows behavior and its valid evidence. Then qualify actual 1.1-to-1.2 upgrades, customization/direct edits, real conflicts, interruption/recovery, repair, rollback and removal on each intended modern profile. Broader legacy native ports and host packages retain their separate staged evidence requirements.

The next brief must state where POSIX cooperation differs from Windows deny-share enforcement and refuse unavailable capabilities. Removing an OS guard without a qualified replacement does not meet this plan. No new storage root, scheduler, importer, harness fork or blanket platform claim is required.
