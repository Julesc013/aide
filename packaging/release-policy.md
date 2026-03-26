# Packaging And Release Policy

## Current Phase

The repository is still in a pre-product and bootstrap phase. This phase defines packaging and release shape only. It does not create packaging automation, signed artifacts, or release binaries.

## Phase Rules

- Packaging records may define artifact classes, manifest placeholders, release channels, and signing posture.
- Packaging records must not imply that artifacts are currently built or shipped unless actual release work later records them.
- Release records belong in this area only when they reflect real packaging activity.
- Future phases may add manifests, signing flows, notarization procedures, and actual artifact generation when implementation maturity supports them.

## Repository Posture

- Final release artifacts are not stored in Git by default.
- Packaging matrices and catalogs express posture, not shipment.
- Historical or archival lanes may use different release shapes than modern native-extension lanes.
