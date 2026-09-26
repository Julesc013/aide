# Importer runtime diagnosis and fixture scope

The first selected batch was TIMEOUT at 180 seconds, not a suite pass. Two
completed cases were visible; the controls-race case was unfinished. Exact
receipt: bounded-importer-recovery-check.json. Its single raw log is outside
Git at the path/digest in log_capture; bytes were preserved without whitespace
normalization. Observed scratch 17,542,660 bytes, memory 291,880,960 bytes;
quiescent owned Job, scratch absent, reservation released.

The same real controls-race test then ran alone through the admitted runner
with a finite 300s budget and code-driven thirty-second stack samples. PASS:
one case, 112.647s, exit 0. Receipt: bounded-importer-controls-diagnostic.json,
one external 9,258-byte raw log SHA-256
851073e57e29deb686cd50a9617cddf5ec25f5edb8defd06a7342bc4bdd8596c.
Scratch peak 18,069,781 bytes, Job memory 216,014,848 bytes, scratch absent and
reservation released. Both runs bind real source/input/executable/process
identities. The diagnostic receipt records the staged driver identity and the
aborted pre-run commit; it is not relabeled as a clean source snapshot.

Samples show production os.fsync in windows_guarded_staged_bytes, path
resolution during recovery, then fixture cleanup. No durability check, safety
guard or original assertion is removed. The six pack-based partial-recovery
tests now opt into a smaller valid source fixture, preserving required templates,
changed payload paths, multiple files, real writes and adversarial operations.
The missing-controls process case is unchanged. Full export/archive/consumer
tests keep their original full fixtures. This does not qualify a smaller release
profile or replace final delivered-asset coverage.

Next: freeze this test-oracle delta, run all seven focused cases through the
runner, record results and obtain narrow independent review. Source b325deea's
resource review remains accepted; the oracle delta is a distinct subject.
