# Three-way update source candidate validation

## Frozen files and source boundary

The implementation worker changed only the admitted importer, its tests and
the portable-pack guide in `D:/Projects/AIDE/aide-three-way-update` after
admission commit `63484c7561978aa77fef067e7984164f2ed52946`:

| Path | SHA-256 |
| --- | --- |
| `.aide/scripts/aide_lite.py` | `817f59c4f34f6c92a5a7d6fa8bf752285aee39e8c137123e5cc211cdb74ae69c` |
| `.aide/scripts/tests/test_export_import.py` | `d925076719d9662ef752a11ec0f78cd8c775f2beee420ae4664904da7003d96f` |
| `docs/reference/cross-repo-pack-export-import.md` | `165a9698d0ed88c6861953b1c7bb41f6f4a2bba7431cbced30aca65e68d91ac3` |

External implementation handoff
`D:/Projects/AIDE/_review_scratch/three-way-update-implementation/implementation-handoff.md`
has SHA-256 `513cc21f512e9492cb8a5455499b26e34aedefe6af0ed738d0970e780d67465c`.
The owner delegation and WorkUnit ExecPlan govern this code, not the handoff
note. No source commit, artifact regeneration or dev effect preceded this
validation record.

## Implemented behavior

- Read v1 and v2 receipts; write v2 with separate installed/source digests,
  project overlay state, disabled feature IDs and project-controls digest.
- Preserve direct edits when upstream is unchanged. Require exact predecessor
  and plan-bound manual `--resolve TARGET FILE` / Python `resolutions` for a
  receipt-owned changed-upstream conflict. Refuse implicit recreation of a
  missing receipt-owned file. Keep resolution bytes in verified bounded
  single-link Windows input memory; store digests, not raw bytes or file path,
  in the durable intent and feedback.
- Admit only project-owned `local_state_examples` disable over
  `.aide.local.example/`, preserve its bytes across updates, refuse malformed
  controls and unknown IDs, and keep absent/stale rationale `unknown`.
- Preserve overlays at removal, refuse overlay/skipped repair and unsafe
  rollback, retain interrupted intents on uncertain effects, and refuse new
  explicit resolution/disable apply outside Windows. Dry-run stays available.

## Executed focused checks and limits

- The six control/resolution cases passed 6/6 in 267.850 seconds, exit 0,
  log SHA-256 `510432cc71a3a8388ca79819e156343c33ecf2bd2a56b058528fe5acdd3307c6`.
- Eight importer/lifecycle interoperability cases passed 8/8 in 257.455
  seconds, exit 0, log SHA-256
  `655c1393d053eee402024f09cc85ad46dfa45bcd8af0c333ca746348dfc398f7`.
- Those 14 cases bind source SHA-256
  `6ea0fb8a4792886c50acdf3dfbf4cf83c58d2c1e8870c45f818e4d08bf6af981`
  and test SHA-256 `d9250767...`. The only subsequent source delta added the
  narrow non-Windows apply refusal. Two affected Windows cases were rerun on
  final source/test/doc hashes above and passed 2/2 in 94.035 seconds, exit
  0, log SHA-256 `f40bbe4a6cfd1c7ae71a8969ce31c237006993e5cfb04aa7ce25af4a4b9d9504`.
- Python AST parsing and `git diff --check` passed on the final files. All
  logs are under `D:/Projects/AIDE/_review_scratch/three-way-update-implementation/`.

These are source-level results. Independent technical review, full affected
suite, new pack/release bytes, extracted consumers, replay and dev effect are
still pending. Earlier superseded source/test logs remain external and are
not counted as final-hash qualification.
