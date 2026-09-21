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

Exact removal of 506 untracked archive duplicates awaits review of manifest
`77d6f576f3840971e1b9b470dd809819963662c0ac4c1009dfc5372f72b11029`.
Tracked generated-output retention remains a separate unresolved policy issue.
