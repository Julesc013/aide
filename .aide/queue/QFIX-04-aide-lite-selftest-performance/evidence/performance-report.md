# Performance Report

## Baseline

- `py -3 .aide/scripts/aide_lite.py test`: approximately 152 seconds in the prior validated run.
- `py -3 -m cProfile .aide/scripts/aide_lite.py test`: 245.014 profiled seconds before the selftest golden-task reduction.
- Top profiled cost before the change: `run_golden_tasks`, 191.396 cumulative seconds.

## Changes

- Added `SELFTEST_GOLDEN_TASK_IDS` for representative selftest golden-task smoke coverage.
- Extended `run_golden_tasks` to accept `task_ids` while preserving existing full-catalog behavior when no task selection is provided.
- Changed `run_selftest` to run the representative smoke set instead of the full catalog.
- Reused one `run_context()` output for snapshot, repo-map, test-map, and context-packet selftest checks.
- Added `pattern_matches_normalized` so `is_ignored` normalizes candidate paths once instead of once per pattern.
- Changed golden-task report unit tests to use a deterministic 10-task subset for report rendering and determinism checks; full catalog coverage remains under `eval run`.

## Result

- `py -3 .aide/scripts/aide_lite.py test`: 28.160 seconds after optimization in this workspace.
- `py -3 .aide/scripts/tests/test_golden_tasks.py`: 91.330 seconds after replacing repeated full-catalog report runs with a report-smoke subset.
- Full `eval run` remains available and was not replaced by the selftest smoke set.

## Boundary

- No provider calls.
- No model calls.
- No network calls.
- No target repo mutation.
- No broad repo-wide rewrite.
