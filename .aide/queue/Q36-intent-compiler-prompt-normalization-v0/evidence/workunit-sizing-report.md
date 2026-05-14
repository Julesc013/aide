# Q36 WorkUnit Sizing Report

`.aide/policies/workunit-sizing.yaml` defines the Q36 sizing model.

## Sizing Classes

- `one_shot`: one subsystem, clear allowed paths, clear validation, no destructive ambiguity, no external credential, no broad migration.
- `two_shot`: first WorkUnit makes the task deterministic; second WorkUnit implements.
- `refactor_gate`: structure changes, root moves, tool migration, path rewrites, or ownership-sensitive changes.
- `live_test_gate`: product/runtime behavior, source/network behavior, release behavior, or persisted-state behavior.
- `audit_only`: report/evidence only; no product behavior change.
- `split_required`: multiple subsystems, unclear success, broad refactor, broad product change, or too many unrelated outputs.
- `blocked`: missing credentials, legal/licensing decision, destructive action without approval, or unresolvable manual-content conflict.

## Required First Steps

Inventory/classification is required before:

- root moves or root deletion;
- broad cleanup or broad refactor;
- tool absorption/migration;
- target install/upgrade/rollback;
- release or production-readiness claims;
- behavior claims without runnable proof.

## Behavior Proof

Artifact existence is insufficient when a prompt implies product/runtime
behavior, release readiness, production readiness, source/network behavior,
persisted state, branch promotion, install success, or target-repo safety.

## User Questions

Q36 asks the user only after repo-state reconciliation. Repeated, partial, or
out-of-order prompts first consult queue state, latest task packets, task
resumption policy, WorkUnit policy, recovery policy, and branch policy.
