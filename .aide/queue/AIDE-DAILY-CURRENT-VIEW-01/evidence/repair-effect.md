# Final affected qualification

First job 6783c56bed3a448ca49be723cf18def5 ran 51 methods, with zero failures,
eight errors across five new methods, and zero skips. Every error arose from
the new fixture bypassing main() and passing a string instead of a Path.
The original 29 methods passed. Collection digests, quiescence, scratch absence
and reservation release are verified; retain the failed job unchanged.

Change only the new command fixture to call the real main() entry point and
the task-local wrapper to run the affected 22 methods, then all three originally
required actual CLI subprocess smokes. No assertion is removed. Product source,
original test bytes and required smoke assertions remain identical to c7ea89dc.
Reuse the 29 passing original methods under those identical inputs.

The repair-job-template pins the first result plus the original input set. After
exact independent review and guarded commit, substitute only source_commit/tree.
Use the same isolated controller, imported-source guards, config, budgets, shared
admission and collection/retirement checks. This is the second and final job;
no further retries are admitted. Final outcome review remains required.
