# Readable complete validation qualification

`validate` now shows total/severity counts and every non-PASS finding. `--full`
retains the previous complete text; `--json` supplies every ordered message in a
versioned object. Validators, their assertions and exit semantics are unchanged.
Only command presentation and argument parsing changed in the implementation.

Actual repository comparison: **60,915 checks, 4,894,325 full bytes, 241 compact
bytes**. All 60,914 passes remain counted and the one warning remains visible.
This measures output size and finding preservation, not execution speed, token
billing or whole-task efficiency. JSON retains duplicates and Unicode. Automated
consumers needing individual PASS lines must use --full or --json.

| Allocation | Outcome | Evidence |
|---|---|---|
| 1, 9ae91713 | PASS: 36 source tests | evidence/source-attempt-01.json |
| 2, 7bc80cbd | FAILED_PRESERVED: 36 delivered tests had one fixture error and one failure; ownership/export checks passed | evidence/pack-attempt-02.json |
| 3, 939d11f6 | FAILED_PRESERVED: 10 source tests had missing AGENTS fixture target; no export | evidence/repair-attempt-03.json |
| 4, b0880db0 | PASS: 10 source, 36 delivered and six ownership tests and actual output comparison | evidence/repair-target-attempt-04.json |
| 5, 6b1503ea | PASS exact six-commit preview; qualified pack unchanged | evidence/preview-attempt-05.json |

All allocations are retired/quiescent, collection digests verified, scratch absent
and reservations released. Original failures remain intact. No failure was turned
into an expected pass or skip. The two fixture repairs preserve every original
behavioral assertion: an ordinary project has its own memory/instructions; a
re-export fixture explicitly supplies its import policy. The 10 source tests cover nine new
methods plus the repaired existing method. The other 26 unchanged source methods
retain their original passing evidence. All 36 delivered methods ran successfully.

Implementation binds c96577f7b079a00dbedbb580c289759a21d02fec. Final test repair and
export qualification bind 0dc7d2a0f439bab0f826a4118697beeb928a3763. The final 865-member
pack adds the validation-output test and changes CLI, Lite reference and the
existing re-export fixture test, plus derived metadata. Exact final payload hashes
are in evidence/attempt-04-delivered-result.json. Capability binding is CURRENT,
classifications unchanged. Published Lite 1.0.0 assets and live context are unchanged.

Fixed preview covers 21625bd6a5cf9610e3b8a5a586fb1290bcdf6fe8 through
13edc23c88d5db9440f2256a0b178b3d14f5cc96 (six commits, zero malformed). Terminal
closure is checked separately through the complete integration range. Preview
is not an official release. The historical global review-packet missing-reference
warning remains; this task's review packet links the existing review procedure.

No live target adoption, host binding, model execution or new release is claimed.
Native downstream ownership and desktop binding retain their existing blockers;
whole-outcome cost remains unknown. This bounded usability increment does not
complete the larger daily-use campaign.

The exact integration effect and actual Git refs govern dev/main synchronization.
The local evidence/integration-result.log records performed effects; planned
integration is not treated as execution. Only this local task branch may retire.
