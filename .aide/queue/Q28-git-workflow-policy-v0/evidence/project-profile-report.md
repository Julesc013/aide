# Q28 Project Profile Report

## Profiles Added

- `aide`: strict trunk plus `dev` integration when multi-agent/multi-machine sharing requires it; SemVer hints for contracts/tools.
- `eureka`: `main` canonical and `dev` integration/quarantine for waves with production-reality gates.
- `dominium`: `dev` integration useful; release branches justified for shipped builds/content/save compatibility.
- `website`: simple GitHub Flow by default; `gh-pages` only when deployment mode requires it.
- `native_client`: `main` canonical with optional `dev`; release branches when shipped binaries require maintained lines.
- `connector_heavy_repo`: `main` canonical, `dev` integration for adapter waves, connector isolation through task branches.
- `data_snapshot_repo`: `main` canonical, conservative data/snapshot changes, release branches only for maintained snapshots.
- `unknown_repo`: conservative profile with no mutation recommendation until inspected.

## Why They Differ

The profiles preserve the common law that `main` is canonical and `dev` is
integration, while leaving room for shipped-game release lines, website deploy
branches, connector-heavy review pressure, or data-snapshot retention. Q28 does
not force full GitFlow onto AIDE/Eureka or unknown repositories.
