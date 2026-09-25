# Validation

- PASS: `py -3 -B .aide/scripts/aide_lite.py validate` on the admission
  worktree (exit 0). Exact admission commit `5f2441d1` passed structured
  commit-message precheck and latest-commit check.
- PASS: three external extracted-ZIP canaries in `forced-restart-canaries.md`
  exited 0 in their final runs: four completed-effect recoveries after child
  process exit 77 and one first-payload safe refusal after exit 77. Their
  summaries, scripts and logs have exact SHA-256 values in that record.
- PASS_WITH_NOTES: independent reviewer `/root/customization_review` accepted
  the local canary evidence only; report SHA-256
  `bbdccecd9f7c885a30eb1b6528e355938bdbc959ff70a2a0443ed56e7e6f0dbf`.
- FAIL retained: two earlier combined harness runs used incorrect runner and
  authored-AGENTS expectations. Exact logs and failure files remain external;
  corrected final run passed without product source changes.
- OPEN: full partial-import recovery, final downloaded-byte consumers, OS
  network trace, hostile timing and stable release acceptance.
