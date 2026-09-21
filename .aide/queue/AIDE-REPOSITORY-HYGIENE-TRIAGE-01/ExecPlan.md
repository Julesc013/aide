# ExecPlan: Repository Hygiene Triage

## Objective

Reduce Git status noise and establish an evidence-backed retention model for
the repository's large `.aide/` footprint.

## Scope

- Classify tracked and untracked bytes by owner, kind, reproducibility, and custody.
- Suppress only loose expansions already preserved in verified tracked archives.
- Preserve unique dirty work and externally recoverable snapshots.
- Produce exact follow-on dispositions for generated reports and repeated logs.

## Progress

- [x] Create and restore-test an external dirty-state snapshot.
- [x] Inventory 10,924 tracked files and the original 714 untracked files.
- [x] Measure tracked and untracked duplicate content.
- [x] Verify two passed Facman custody archives and their 102 loose expansions.
- [x] Classify active broker, isolated-host, and entry-restart evidence.
- [ ] Decide generated-report retention and regeneration policy.
- [x] Prepare destructive cleanup as an exact reviewed apply set.

## Verification Intent

Use the repository's own repo, quality, refactor, and roots commands plus
byte-level SHA-256 and ZIP member verification. Do not infer deletion safety
from age, size, orphan status, or duplicate status alone.

## Blockers

Exact removal of 506 untracked archive duplicates awaits review of the canonical
committed manifest SHA-256
`381213944009ef69aa4860ccb4269b9a0ecd72091fe3f0cb5fa41de40dcfe47d`.
Tracked generated-output retention remains a separate unresolved policy issue.
