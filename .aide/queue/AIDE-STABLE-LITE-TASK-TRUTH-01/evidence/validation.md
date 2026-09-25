# Validation, 2026-09-25

- RED before implementation: `py -3 -B -m unittest discover -s
  .aide/scripts/tests -p test_x_os_01_task_os_commands.py -k
  empty_target_packet -v` exited 1. The newly added regression expected no
  latest task, but unmodified source returned `X-OS-01` from contextual text.
- PASS after implementation: the full focused X-OS-01 suite ran 9 tests and
  exited 0, including the clean-target, explicit packet-ID, leading PHASE,
  no-apply and golden tests. Durable external log:
  `D:/Projects/AIDE/_review_scratch/stable-lite-task-truth-20260925/x-os-01-focused.log`,
  SHA-256 `404211bb3c54f3d3c852a85e38736cc372869af6294c609667dc19ff225b75bc`.
- PASS: `py -3 -B -m unittest discover -s .aide/scripts/tests -p
  test_x_os_02_capability_reality.py -v` ran 5 tests, exit 0.
- PASS: `py -3 -B -c "import ast,pathlib;
  ast.parse(pathlib.Path('.aide/scripts/aide_lite.py').read_text(encoding='utf-8'));
  print('syntax: PASS')"` exited 0.
- PASS: `py -3 -B .aide/scripts/aide_lite.py validate` exited 0 and reported
  `status: PASS`. It produced very large output; only its status is claimed.
- PASS: `py -3 -B .aide/scripts/aide_lite.py doctor` exited 0 and reported
  `status: PASS`. Durable external log SHA-256
  `f5dcaac6669fb35667c33ecbf2e1b45edbd4ff7308e1adfd851f90939ae09d8d`.
- PASS: `git diff --check` found no whitespace errors before candidate freeze.
- NOT RUN here: current-generator archive projection, installed-byte retest,
  replay, final release suite, main promotion, publication and downloaded
  consumer acquisition. These belong to later gates.
