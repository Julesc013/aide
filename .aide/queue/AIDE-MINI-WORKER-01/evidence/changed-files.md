**Scope:** one optional, source-only Mini worker binding and its qualification.

- `core/execution/mini_worker.py`: exact dependency/attempt identity, lazy upstream
  DefaultAgent use and an independent AIDE receipt. Disabled unless explicitly enabled.
- `core/execution/tests/test_mini_worker.py` and task runners: actual upstream-loop
  repair, refusal, failure, cancellation and continuation fixtures; bounded
  acquisition and retained evidence checks.
- Task records, queue index, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md` and
  `docs/reference/mini-worker.md`: scope, outcomes, recovery and unresolved limits.
- Six `.aide/changelog/` outputs: reviewed five-commit preview through `cf77e790`.

[Fixture source](fixture-source.json), [final-check source](final-source.json)
and [closure source](closure-source.json) bind exact files and hashes. The closure
map covers the remaining metadata; the earlier maps preserve executed source.
All 870 development-pack files and eight frozen release assets remain unchanged.
Existing runtime owners, target repositories and live endpoints are outside this diff.
