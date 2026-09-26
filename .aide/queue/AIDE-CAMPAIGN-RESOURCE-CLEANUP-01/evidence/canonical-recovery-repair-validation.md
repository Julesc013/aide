# Canonical recovery review repair

Independent REQUEST_CHANGES for 8acfecc44e61cbc9ac13c9fa9f773c7d5b43906b,
tree 1edfe2562ce980404a9f4439e1fda421d9240d0c, is retained in review-8acfecc4.md.
External original SHA-256:
216ce13de0fc506c949f1ea47d2e46f0d5269e7628706da19b9ab2da9b79ff11.

Required repair: recovery of a persisted quiescent exited/0 checkpoint must not
bypass final canonical limits or identity. Both run and recover now call the
same final qualification. Root and volume declarations are rechecked; overrun
or changed identity becomes canonical_output_limit_or_identity, with the actual
prior process result retained. Canonical contents are never cleanup targets.
Monitor scans also compare declared volume identities before tree enumeration.

Command with explicit existing tiny-fixture parent, Windows/Python 3.14:

    py -3 -B -m unittest discover -s .aide/scripts/tests -p test_managed_workspace.py -k canonical -k success_retires -k controller_crash -k interrupted_retirement -v

PASS: ten affected tests, no skips, 13.276 seconds, exit 0. New crash-boundary
regressions use a tiny simulated completed host and real recovery, reproducing
the formerly successful quiescent checkpoint on over-budget output and changed
volume. Existing real process overrun, crash, retirement, junction and admission
cases also pass. Syntax and git diff --check pass. Fixtures retired.

The prior 22-case run remains prior-source evidence. No new full importer suite,
package build, integration or release acceptance is asserted. Permanent pool
placement remains unresolved; superseding technical review is the next gate.
