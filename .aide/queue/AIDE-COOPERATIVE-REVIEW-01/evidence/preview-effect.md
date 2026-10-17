# One promotion preview effect

The parent admission permits at most one promotion-only managed allocation.
Commit the independently reviewed staged source unchanged, then substitute only
its actual commit/tree into preview-job-template.json in ignored job input.
Reuse the existing qualified preview owner through run_preview.py; the only
adaptation is fixed base2194eb6b. Generate preview/validate/status once over that
base through the committed checkpoint. Preserve prior six outputs, compare all
other bytes and directory membership, then regenerate exactly in memory.

Unchanged runner configuration61162891 and resource reserves apply: 1GiB memory,
180seconds,32MiB scratch,8MiB retained,1MiB logs and1MiB canonical changelog output.
Collect, verify digests and retire the job. No automatic replacement allocation.
This job does not alter runtime state, product source, packs, releases, providers,
targets or Git refs. Terminal source/generated-byte/Git-effect review follows.
Final evidence-only closure need not recursively regenerate its own preview.
Postpromotion run_preview.py verify is read-only and separately included in the
exact integration effect.
