<!-- Candidate public body. Publish only with the exact accepted effect and assets. -->
# AIDE Lite 1.0.0

AIDE Lite is a repository companion for local planning, context, validation,
and receipt-bound project lifecycle operations. This release's supported
profile is **`aide-lite-local-windows`**, with T3 Limited Support for the
declared Windows and Python environment. The qualified environment is Windows
10 build 19045 with Python 3.14.7. Lifecycle apply is Windows-only.

## Get started

Download `aide-lite-v1.0.0.zip` or `aide-lite-v1.0.0.tar.gz` and verify it
against `aide-lite-v1.0.0.SHA256SUMS.txt`. Extract the archive. Its
`aide-lite-pack-v0/install.md` explains import, update, recovery and removal.
From the extracted `aide-lite-pack-v0` directory, preview a safe import into
a chosen Git repository before applying its exact plan:

```text
py -3 -I -B files/.aide/scripts/aide_lite.py --repo-root <target-repo> import-pack --pack . --target <target-repo> --mode safe --dry-run
py -3 -I -B files/.aide/scripts/aide_lite.py --repo-root <target-repo> import-pack --pack . --target <target-repo> --mode safe --expect-plan <preview-plan-digest>
```

The importer preserves authored target files and requires explicit decisions
for changed ownership or a three-way update conflict. Project-owned
customization metadata and intentionally disabled features persist through
supported updates. Explanations distinguish observed changes from unknown
rationale. Local feedback files are created only when requested and are not
automatically shared.

The CLI also provides bounded partial-import recovery, receipt-owned repair,
rollback and removal for the declared Windows profile. Removal applies only
to proven owned material; keep the extracted pack and receipts for recovery.
There is no declared published predecessor for this first stable version.
The `--from-pack` update path requires the exact validated predecessor pack;
Q47/Q48 preview bundles are not published stable predecessors.

## Limits

- Local CLI operation was tested offline after archive acquisition with a
  Python socket guard. This is not an OS network-isolation guarantee.
- Native hosts, hosted GitHub effects, model/provider operation, autonomous
  workers, and non-Windows lifecycle apply are outside this Lite profile.
- `job usage --attempt-set` reports known supplied-role subtotals and explicit
  gaps. It does not establish complete work totals, internal host requests,
  model billing, or a live Codex turn.
- Testing used disposable fresh and brownfield repositories. Install into
  another project only through that project's own authority and a reviewed
  preview.

## Assets

| Asset | SHA-256 |
| --- | --- |
| `aide-lite-v1.0.0.zip` | `95ecee6c422f07005bf25175aae347b500f2f6343d58c702856a6e977126902f` |
| `aide-lite-v1.0.0.tar.gz` | `16b8c3d19a033d1e6304cad5196a410e7d83d8329c97b54fad0b4602bd1f33a6` |
| `aide-lite-v1.0.0.manifest.json` | `ef116dad9e69d0dc0bea0f2386815add3e6e8ae95dc2e25588ba1d9c3de6d5f9` |
| `aide-lite-v1.0.0.SHA256SUMS.txt` | `1fc39d9b92203a5b62edc26b48939a8b7145b27a1b11f6ead787a1fa49a478c5` |
