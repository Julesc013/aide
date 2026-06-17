# Self-Management Queue Sequence

This is the recommended queue sequence after
`AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01`.

## Review Gates

1. `AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01`
2. `AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01`

## Report-Only Build Tasks

3. `AIDE-BUILD-ROOT-AUTHORITY-MANIFEST-01`

   Define a RootAuthorityManifest schema and seed manifests for current roots.
   Do not move files.

4. `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`

   Detect README, DOCUMENTATION, OKF, queue, protocol, report, and evidence
   drift. Do not edit docs or OKF pages.

5. `AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01`

   Classify generated outputs, generator provenance, source refs, stale status,
   canonicality, and regeneration commands. Do not refresh outputs.

6. `AIDE-BUILD-QUEUE-HEALTH-REPORT-01`

   Report review-gate debt, blocked tasks, supersessions, latest-task drift,
   duplicate tasks, and missing evidence surfaces. Do not accept tasks.

7. `AIDE-BUILD-STRUCTURE-FATE-MAP-01`

   Produce candidate fates for `shared`, `platforms`, `research`, `specs`,
   `.agents`, `.codex`, tracked `.aide/tmp`, and add-only root candidates. Do
   not move or delete files.

## Later Apply Gate

8. `AIDE-BUILD-FIRST-SAFE-STRUCTURE-TRANSACTION-01`

   Apply one tiny, reviewed, low-risk self-management transaction only after
   the relevant manifests, maps, validation plan, and review gates are
   accepted.

## Boundary

This sequence is planning evidence. It does not authorize schemas, commands,
OKF regeneration, generated-output refresh, docs repair, queue acceptance, file
movement, or transaction apply behavior by itself.
