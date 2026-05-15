# QFIX-06 Prompt

Remediate and polish QCHECK-04 warnings that are safely actionable inside AIDE.

The operator asked to fix partial, failed, warning, and blocker states after the
QCHECK-04 checkpoint. This QFIX narrows that broad request to fix-forward work
that can be safely performed inside AIDE now:

- refresh stale generated manifest evidence;
- rerun validation;
- record remaining review-gated states honestly;
- avoid target repo mutation, publication, provider/model calls, branch
  mutation, and install/upgrade/repair/rollback/uninstall apply behavior.
