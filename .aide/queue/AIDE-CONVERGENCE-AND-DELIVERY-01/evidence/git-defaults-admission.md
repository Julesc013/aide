# Portable Git defaults and timely integration

## Owner request and objective

The owner explicitly requested frequent detailed task commits, safe task-to-dev
integration and remote synchronization, followed by reviewed dev-to-main
promotion. The subsequent clarification makes this the default for AIDE itself
and adopting repositories: optional main protection, usually unprotected dev,
short-lived local task branches, publication when collaboration, importance or
blocked continuity warrants it, and removal of obsolete remote task branches.
This is an attributed summary of the conversation, not an external instruction.

Admit AIDE-GIT-DEFAULTS-01 to implement those defaults through existing Git
policy, helper/advisory, adapter guidance and portable export owners. Preserve
project customization, branch naming and stronger existing host protections.
Adoption defaults are not authority to rewrite other repositories or accounts.

## Existing owners and bounded paths

Use .aide/policies/git-workflow.yaml, branch-roles.yaml, branch-protection.yaml,
github-protection.yaml, promotion-rules.yaml and prune-policy.yaml; .aide/git/
helper-policy.yaml, aide-branch-policy.yaml, project-profiles.yaml and their
existing Markdown guides; .aide/scripts/aide_lite.py's Git/advisory owners and
their existing focused tests plus one bounded Git-defaults test module.
No new scheduler, branch database, Git framework or polling service.

Allowed paths after admission:

- .aide/queue/AIDE-GIT-DEFAULTS-01/**
- The six policy files named above; .aide/git/*.yaml and .aide/git/*.md
- .aide/scripts/aide_lite.py
- .aide/scripts/tests/test_q28_git_workflow.py, test_q29_git_helper.py,
  test_q31_export_pack_governance.py, test_q35_github_advisory.py,
  test_git_defaults.py (all under .aide/scripts/tests/)
- AGENTS.md and .aide/adapters/templates/AGENTS.md.template
- docs/reference/git-workflow-policy.md, git-helper-workflow.md,
  branch-roles.md, github-protection-ci-advisory.md
- .aide/queue/index.yaml and parent ExecPlan.md/status.yaml
- README.md, PLANS.md, IMPLEMENT.md, DOCUMENTATION.md
- .aide/intake/latest-*; .aide/context/latest-task-packet.md
- Existing generated/advisory outputs under .aide/generated/**,
  .aide/github/**, .aide/reports/capability-*.json and *.md,
  .aide/verification/latest-verification-report.md
- Derived .aide/export/aide-lite-pack-v0/** after separately reviewed effect

Original acceptance assertions remain unless the requested default deliberately
changes their contract; any changed assertion needs a stated rationale and
independent review. Historical evidence, release assets and tags are preserved.

## Behavior and acceptance

1. Coherent commits retain scope, rationale, validation, risks and follow-up.
   At completed work boundaries, inspect/fetch current refs, integrate qualified
   work to dev and sync, then assess the next qualified main promotion. Avoid
   leaving an accepted chain stranded behind task branches.
2. Hosting protection is a project choice, distinct from never force-pushing or
   deleting canonical/integration history. Main protection is optional; dev is
   normally unprotected. Advisory output must reflect project configuration,
   preserve explicit overrides and never claim remote settings were applied.
3. Task branches are local and short-lived by default. Shared/important/blocked
   checkpoints may be published with an explicit reason and completion boundary.
4. Cleanup considers only exact classified task refs with preserved work, closed
   ownership, no active worktree or open collaboration obligation, and fresh
   containment proof. Keep active, important, persistent and uncertain branches.
   Age alone and a merged flag alone are insufficient. No force or blanket prune.
5. New projects inherit the generic defaults through the existing export/import
   route. Existing project customizations survive update. Prove one configured
   override and one fixture adoption; source declarations alone are insufficient.
6. Keep accepted source, development export and published release identities
   explicit. Main promotion does not relabel an old archive as newly qualified.

## Sequence, finite verification and effects

After exact admission, compile the owner intent, inspect/record the helper plan,
and create local task/aide-git-defaults-01 at the clean accepted current-view
closure in this existing checkout. No clone or new storage root is needed.
Implement the smallest coherent policy/guidance/advisory correction. Qualify
focused positive, override, refusal, conservation and portable-consumer cases.

Use the existing managed runner/config digest 61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90
with unchanged reserves and limits. Maximum three jobs: focused qualification,
derived export/consumer qualification, and at most one reviewed affected repair.
Each exact effect needs independent review and fresh admission. Conserve valid
evidence; preserve any original failure. No models, new dependencies or spending.

Prepare a separate exact integration manifest for the accepted campaign chain
and this child: observed local/remote refs, source and export evidence, checks,
review, other contributors' changes, rollback and verification. After independent
effect acceptance, fast-forward or perform an explicitly reviewed conflict merge
into dev, push non-forcibly, then promote qualified source to main and verify the
remote result. Main/dev may coincide when that exact source is accepted.

Remote task pruning, if warranted, requires its own exact reviewed deletion
manifest with fresh remote and collaboration checks, retained branch/commit
identities and recovery. No open PR, unknown owner, important checkpoint, active
branch, tag, release asset or unrelated repository may be removed by this child.
Existing host protection is never weakened; GitHub configuration apply is out
of scope. Prepare missing distribution/release work as explicit follow-up.

## Stop and recovery

Stop only the affected effect for changed refs, failed required checks, uncertain
ownership, protection refusal or exhausted job allowance. Preserve unrelated
progress. Reconcile actual Git/runner state before retry; never reset or bypass
protection to recover. Source and terminal reviews remain separate from admission.
