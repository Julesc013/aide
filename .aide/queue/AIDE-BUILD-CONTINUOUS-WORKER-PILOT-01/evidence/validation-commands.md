# Validation commands

Python: C:\Program Files\Python314\python.exe (WindowsApps py launcher was unavailable in sandbox).

- python -m unittest discover -s .aide/scripts/tests -p test_continuous_worker*.py -v: 51 passing tests; unit-tests.txt.
- AST parse of eight runtime Python files: passed.
- git diff --check: passed.
- aide_lite.py intent compile / task inspect / task noop-check / task recover: recorded before queue admission.
- aide_lite.py doctor and validate: global export/pack checksum failures recorded separately.
- aide_lite.py git policy / git detect / git plan: report-only; no branch mutation.
- aide_lite.py pack --task AIDE-BUILD-CONTINUOUS-WORKER-PILOT-01: passed task-packet budget.
- FacMan tools/workspace_hygiene.py paths and doctor --measure: passed.
