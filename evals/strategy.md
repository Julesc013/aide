# Evaluation Strategy

## Purpose

AIDE needs layered verification because it spans modern and historical hosts, multiple execution modes, and uneven host capability ceilings. The evaluation framework must scale from early structural checks to later behavioral evidence without pretending that current coverage is deeper than it is.

## Layered Verification

The strategy for this phase is:

1. establish deterministic structural verification
2. keep schema and documentation consistency explicit
3. define smoke and packaging categories before implementation exists
4. add deeper behavioral evals only when implementation and environments make them meaningful

This keeps early progress auditable without fabricating runtime coverage.

## Host-Family Differences

Evaluation depth will differ by host family and adapter technology:

- modern native-extension lanes may eventually justify stronger load, editor, workspace, packaging, and release evals
- archival or companion-oriented lanes may rely more heavily on structural, provenance, or archival-record verification
- historical lanes may require environment or media evidence before smoke verification is even possible

The matrices should therefore track posture conservatively rather than assuming uniform parity.

## Historical And Archival Evidence

Historical or archival lanes may need different evidence types than modern lanes. Examples include:

- preserved manuals or manifests
- reproducible environment records
- provenance or extraction notes
- documentation consistency checks that map known lane intent to available evidence

This is still verification, but it is not the same as modern runtime integration testing.

## Growth Rule

Future prompts should expand eval coverage by:

- adding stable eval definitions to catalogs
- recording concrete evidence expectations
- updating matrices only when evidence or implementation changes justify it
- preferring explicit `blocked`, `deferred`, or `unverifiable` states over optimistic claims

No phase should claim passing coverage for behavior that has not been run.
