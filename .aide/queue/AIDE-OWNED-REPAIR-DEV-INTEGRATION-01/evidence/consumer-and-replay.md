# Exact artifact consumers and zero-change replay

The frozen source/artifact candidate is `e4697aaa327189e6eb00742613de841aa4e4d4a8`,
tree `a0b2ed700ee89da3200f00ed2591e8860b75be06`. Its portable
source remains `71501c6bb30bb19a6f7cb0056ba0f009d39a9b40`.

Independent offline artifact qualification used the exact local ZIP
`33cb8c061e32cc82853948bdf7f43bf750db34ef1da395a2ce3b857c7d532e90`
and tar.gz `bcafe450eaf7ef49d16a3b446bd2347fc644b1a675d1a304cff131619bbf99db`.
Both hashes remained unchanged after consumers. The two archives have 833
identical safe regular-file names and bytes. All 830 projected pack checksum
entries and seven release checksum entries match.

The archive intentionally excludes the source export path
`files/.aide.local.example/secrets/README.md` under the release
forbidden-path policy and rebuilds projected metadata. Source export
manifest/checksum hashes in release provenance bind the full export pack;
all 827 archive payload files match the common source export files exactly.

A fresh extracted ZIP and a brownfield extracted tar each passed eight offline
CLI checks: import preview/apply, installed CLI doctor, read-only removal
planning, one missing receipt-owned file repair preview/apply, direct-edit
conflict preservation, and post-edit read-only removal planning. The
brownfield authored `AGENTS.md` prefix remained byte-identical while the
managed section was added; authored unknown.txt and project-state content
remained intact. The brownfield removal plan's exit 2 is the expected
`PRESERVATION_REQUIRED` result. No outside target or network effect ran.

The independent consumer's durable record is
`D:/Projects/AIDE/_review_scratch/owned-repair-consumer-71501c6b/final-evidence.json`
(SHA-256 `46fce265a7d17cbf144a985bf6c1e43ec9250ca90cf1c3c10e6f6f9dfb4c0d8d`),
which binds all 16 command logs and exits. Supporting records:
`archive-verification.json` SHA
`6104b33ed2af3aa210fdf1890f8af63ff7eeec2097ae7ead1ad5fed79c479b6a`,
`artifact-classification.json` SHA
`090db764d37124744c94cfad737606e3d811304c9848f726872aab329e3c8dff`,
and `consumer-summary.json` SHA
`f0f76ad8e3202ff73b99fb940a674422c710372bcbf19857a7d8c5a9f2f23039`.
Extracted fixtures and logs remain in that external directory.

From clean convergence commit `e4697aaa`, `release bundle`, `release
validate`, `release draft`, and `release draft-validate` all exited zero.
The 44 tracked release files changed zero bytes; the before and after
path/hash lists both hash to
`310a42cc6e8420d266a95e205ff3f64d787a23fdc5960a80421793ca8724b749`.
Final canonical validate, doctor, pack-status `PASS_SOURCE_ANCESTOR`,
and nine-commit range checks all passed. No source, archive, or release byte
changed during these read-only checks. This is dev-integration evidence, not
main, native/hosted, or stable-publication acceptance.
