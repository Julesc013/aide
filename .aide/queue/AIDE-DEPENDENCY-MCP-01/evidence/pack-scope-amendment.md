# Development provenance closure within the remaining allocation

After committed source3d789913, final validation reports exactly two failures:
export provenance and pack-status reject prior source1435659b. The conservative
ancestor check treats any change under PORTABLE_SOURCE_DIRS as affecting the
pack, including the new test_continuous_worker_mcp.py excluded by the existing
source-only test convention. The current payload is expected byte-identical.
Do not change support claims or bypass the provenance check.

Extend this child's allowed paths only with .aide/export/aide-lite-pack-v0/**,
generated through the existing owned exporter. Prepare one task-local wrapper
around AIDE-DAILY-PACK-REFRESH-01/run_refresh.py and its pack_inventory/six ownership
checks. Pin exact complete predecessor inventory. Reuse the already admitted
second allocation (maximum two total), separately reviewed source/effect; do not
allocate a third or repeat the 60 unchanged runtime tests.

Before generation, verify ordinary owned descendants, exact Git identities and
checksums; preserve metadata and recoverable Git blobs. Run existing export-pack,
doctor, validate and pack-status. Compare every payload/checksum byte before and
after, permitting only manifest.yaml and export-report.md provenance changes.
Unexpected payload change fails and is preserved for inspection, never silently
accepted. Compare all four published1.0.0 assets byte-identically. No archive build.

Unchanged runner config61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90,
1GiB/180seconds/32MiB scratch/8MiB retained, 7MiB canonical export reservation and
existing reserves. No changelog, source, target, network, live peer, install,
provider, release or configuration effect. Collect/retire and preserve original
validation failures and actual outcomes before exact terminal integration review.

This demonstrates metadata closure only. Existing payload consumers and the 60
source interface cases retain their exact identities. The repeated conservative
source-only-file invalidation is a bounded future improvement candidate, not an
excuse to alter the validator or expand Lite in this child.
