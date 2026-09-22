# Changed files

The 2026-09-22 source slice adds
`core/runtime/integration_broker/github_merge.py`, extends only the admitted
GitHub observation test, updates this task's living records and queue index, and
updates the broker/root documentation indexes. It does not add a sender,
credential source, workflow, settings apply, branch mutation or hosted effect.

The target-policy source slice adds
`core/runtime/integration_broker/github_target_policy.py`, extends the existing
GitHub observation test with policy-plan fixtures, adds desired/current/plan and
refreshed-observation evidence, and updates this task plus existing broker/root
documentation. It does not add `.github/workflows/**`, a sender, credential
source, settings apply, branch mutation or hosted effect.

The publication receipt adds only exact branch, commit, tree, remote
observation, and retained-gate facts for the source checkpoint.
