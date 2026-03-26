# Release Checklist

## Artifact Naming

- Confirm artifact names follow the packaging naming policy.
- Confirm exact host versions appear only where concrete artifacts or release records justify them.

## Manifest Completeness

- Confirm required manifest placeholders or manifest files exist for the scoped release shape.
- Record any unresolved manifest fields explicitly.

## Signing Or Notarization Posture Review

- Confirm the expected signing posture for the scoped lane.
- Record `required`, `deferred`, `not-required`, or `unknown` honestly.

## Matrix And Catalog Alignment

- Confirm packaging catalogs, release records, and packaging matrices agree on posture.
- Confirm no file implies built artifacts that do not exist.

## Release-Note And Documentation Alignment

- Confirm release records and supporting docs describe the same scope and status.
- Keep release documentation audit-oriented and factual.

## Deferred And Blocker Capture

- Record missing manifests, signing gaps, missing build outputs, or release blockers explicitly.
- Distinguish intentionally deferred release work from blocked release work.
