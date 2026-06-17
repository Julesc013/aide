# Validation

Commands run:

- `git status --short --branch`: PASS before edits; clean on `main`, ahead of
  `origin/main` by one existing commit.
- `py -3 .aide/scripts/aide_lite.py git plan`: PASS as dry-run plan;
  `ready_dry_run`, no apply, no push, no remote mutation.
- `py -3 .aide/scripts/aide_lite.py intent compile --prompt "...legal docs..."`:
  PASS; docs, low risk, audit-only sizing, safe to execute, not blocked.
- Official Apache-2.0/SPDX/DCO reference check: PASS for confirming
  Apache-2.0 identifier, license posture, contribution section, and trademark
  boundary.
- `Compare-Object C:/Downloads/AIDE_LICENSE_APACHE_2_0.md LICENSE.md`: PASS
  with only the removed leading blank line from the downloaded draft observed.
- `git diff --check`: PASS with Git's known CRLF normalization warning for
  `.aide/queue/index.yaml`.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py intent validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ADOPT-APACHE-2-LICENSE-01`:
  PASS; status `needs_review`, classification `complete`, evidence files 6,
  missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ADOPT-APACHE-2-LICENSE-01`:
  PASS; all six evidence files listed, no missing evidence.

Post-commit validation:

- `py -3 .aide/scripts/aide_lite.py commit check --latest` must be run after
  commit creation.
