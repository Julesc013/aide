# AIDE Packaging

`packaging/` is the control plane for AIDE artifact classes, manifest placeholders, release channels, signing posture, and release records.

This area differs from:

- `hosts/`, which describes adapter lanes and host-specific integration surfaces
- `shared/`, which describes shared implementation boundaries and contract shapes
- `environments/`, which tracks concrete runnable setups, media, toolchains, and snapshots

`packaging/` records packaging models, catalogs, manifest placeholders, release records, and audit procedures. Source directory names remain compatibility-technology based even when produced artifact names later include exact host versions.
