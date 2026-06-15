# Recommended Next Work

1. `AIDE-ACCEPT-TESTJOB-SCHEMA-01`
   - Accept or reject the minimal metadata-only TestJob schema slice after this independent check.

2. `AIDE-BUILD-REFERENCE-ID-SCHEME-01`
   - Per the user-supplied frozen sequence, build stable reference IDs after TestJob acceptance.

Do not proceed to PatchTransaction before ReferenceID and EventRecord work unless a later reviewed queue item changes the sequence.
