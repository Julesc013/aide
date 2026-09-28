# Portable attempt attribution

- Base: `dev@dbf216c3e0ce9d03dda9dec8045c21366182ea6e`, tree `2f067678e6bab260c81b84880a7973f983903e7c`.
- Scope: existing `job usage` CLI, focused tests, runner guide and this WorkUnit. No model call or target mutation.
- Red: configured D-managed job `3b4489de18ec4a4f947df8cdd47d0270` ran `python -m unittest discover -s .aide/scripts/tests -p test_efficiency_wait.py -v`; 22 cases, four new expected errors from absent attribution function, 18 existing cases passed. Receipt SHA-256 `f075c055f7231e14aaca765dffa82966ed5169206634b5310cbd3c8ff70fc378`.
- Green: same bounded command, job `1f2be7e779b04a89aaf613b40e7356a2`; 22/22 passed. Receipt SHA-256 `370a05f0a89ecf6abaa6659d06452bc36d4c515d28717dc08da1605f9b6e22ac`. Observed peak memory 330,117,120 bytes; scratch 4,045 bytes. The receipt phase is `retired`; scratch was absent after the run.
- Input: one to eight explicitly supplied ordinary Codex `exec --json` streams, bound to a bounded JSON roster by exact SHA-256 and relative path. The roster declares one parent and child/review/retry/repair/overhead attempts with unique IDs and acyclic parent links. Missing streams and same-session overlap remain explicit.
- Output: supplied known token subtotals by role, stream digests and compact terminal states. Complete work totals, work outcome, internal model requests and unlisted attempt coverage remain unknown. No raw stream content or path is written to Git or emitted in the accepted result.
- Still pending: independent exact-source review, dev integration, refreshed delivered-byte qualification and separate real-host permission/effect. This does not establish stable release acceptance.
