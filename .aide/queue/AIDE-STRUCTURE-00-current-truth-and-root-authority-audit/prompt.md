# Prompt

According to the 2026-06-17 structure note and live repo doctrine, do not
immediately shuffle files. First define the current truth and root authority
picture, reconcile stale or mismatched generated status, and use AIDE's
existing no-apply repo/root/refactor machinery before any future moves.

Perform the first task now:

`AIDE-STRUCTURE-00-current-truth-and-root-authority-audit`

The task is read-only/check-only. It must produce evidence-backed reports and
stop at review. It must not move files, delete files, rewrite references,
create new top-level roots, promote generated outputs to source truth, mutate
branches, mutate target repositories, call providers/models, call the network,
or claim release/product readiness.
