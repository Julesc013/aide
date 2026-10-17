# Export qualification interruption

Job425afc83 exited1 and is retired, quiescent, digest-verified with scratch absent
and reservation released. Ownership6, existing export, doctor, fullvalidate and
pack-status passed. Membership stayed862. Only CLI and binding-test payload plus
manifest/checksums changed. The source reference document is not an export member
in either prior or resulting pack. The wrapper incorrectly required its change;
that assertion stopped before delivered tests. No delivered pass is claimed.

Correct the wrapper expectation to the actual two exported payloads. Keep the
reference in source documentation. Preserve the successful export unchanged and
all original runtime assertions. Final allocation3 will verify full exported hashes,
run delivered60, then generate the existing fixed preview in one bounded job.
No export rebuild, source rerun or fourth job. This is a reviewed continuation
proposal, not an automatic retry. Original failed runner is retained atbf15170f.
