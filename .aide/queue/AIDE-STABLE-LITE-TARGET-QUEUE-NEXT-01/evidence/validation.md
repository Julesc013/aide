# Validation, 2026-09-25

- RED: `py -3 -B -m unittest discover -s .aide/scripts/tests -p
  test_x_os_01_task_os_commands.py -k nonempty_target_queue -v` exited 1
  before implementation. The one-item target fixture received
  `X-OS-01 - Task OS Report-Only Commands` instead of target-owned advice.
- Initial green change passed the new test but failed the existing post-apply
  source fixture because that fixture lacked early X-OS items. The source
  routing identity set was expanded to include its exact post-apply records;
  that failed full-suite attempt remains part of the validation history.
- PASS: the final focused Task OS suite ran 10 tests and exited 0. It covers
  zero- and one-item targets, explicit/leading packet IDs, source X-OS and
  post-apply routing, no-apply reports, and golden runners. External log:
  `D:/Projects/AIDE/_review_scratch/stable-lite-target-queue-next-20260925/x-os-01-focused.log`,
  SHA-256 `6217fc734c1bf44cf1738d1b21286c55216af4861345c29a14dac23635437be7`.
- PASS: Python AST parse of `.aide/scripts/aide_lite.py` exited 0.
- FAIL, retained as projection gate: `py -3 -B .aide/scripts/aide_lite.py
  validate` exited 1, SHA-256 log
  `3015a89c5c985bd69736bb1e1a105813bfab6916e8572e3489a78b2c4ef4866d`.
  Its two failures are export manifest source provenance and pack-status:
  archived source `8365aa61` does not match current source `04caefe6`.
- FAIL, same dependency: `py -3 -B .aide/scripts/aide_lite.py doctor`
  exited 1, log SHA-256
  `fd0005b0ffa2a75dfa89b1db43c69cb4ad8de69a527ee4da1ae3319c1c0cdf87`;
  its single failure says validation needs repair. The source WorkUnit forbids
  regenerating the archive; the later projection must clear both failures.
- PASS: `git diff --check` found no whitespace errors before candidate freeze.
- NOT RUN: current-generator artifact projection, installed target recheck,
  replay, dev effect, final release and downloaded-asset acceptance.
