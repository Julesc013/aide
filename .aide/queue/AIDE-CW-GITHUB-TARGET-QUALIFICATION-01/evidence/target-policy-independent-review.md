# GitHub Target-Policy Independent Review

Date: 2026-09-22

## Outcome

`REQUEST_CHANGES`

The committed unresolved packet is fail-closed today: it records
`broker_principal_unresolved` and `workflow_check_identity_unresolved`, contains
zero operations, sets `apply_authorized` to `false`, and does not install a
sender, credential path, workflow, or settings mutation. The resolved contract
is not ready for consequential use, however. Three P1 defects and one P2 defect
remain in the exact source under review.

This review does not authorize target mutation, workflow or ruleset
installation, credential or principal creation, hosted effects, branch changes,
push, merge, tag, or release.

## Exact Review Subject

- Base: `c6fdc754844cf7d42302218ce08307a7e05dcb61`, tree
  `acb1ff296a622cc614e71b3ebb17a23752f8d902`.
- Source: `bb433bb74f645e0904ca34bf3af38516ae05a7ad`, tree
  `a871c65880161f147f35cf8df7269bba9af3a867`, parent exactly the base above.
- Published head: `eb4dea3f30ab53e3e57fe85eae97fa07de6e414c`, tree
  `41adc996349690b4d796d8005ef179c89fb93c8e`, parent exactly the source above.
- The published-head commit does not change
  `github_target_policy.py` or its focused test file relative to the source.
- The exact `base..source` diff contains 18 paths and all are within the task's
  declared allowed paths. `git diff --check` passes.

Reviewed source identities:

- `core/runtime/integration_broker/github_target_policy.py`: Git blob
  `71fd442b22ecdeeb669dfd0673388a0ca372cdb2`; SHA-256
  `b3a08360180f96ec5f2608e478eee7fb22b4876c31b0f4340d1e276c251e2b5b`.
- `.aide/scripts/tests/test_continuous_worker_github_observation.py`: Git blob
  `26dc9a0f4cc5a0bfca7425b450e445d0a8fd8933`; SHA-256
  `2d8306b731940b832df0f6ea5f7991e13e8acb6d6ea3ecf6acda397ea0f293ea`.

## Findings

### P1 F-01: the non-dev ruleset POST body is invalid for the pinned API

`github_target_policy.py:158-163` emits the `update` rule as only
`{"type":"update"}`. GitHub's current `2026-03-10` create-ruleset schema says
that `update.parameters.update_allows_fetch_and_merge` is required. The module
pins that same API version through `github_api.VERSION`. Therefore the generated
`broker_non_dev_confinement` POST is not the claimed exact deployable operation;
GitHub can reject it with validation failure. The focused test at lines 667-670
asserts only the rule-type list and consequently blesses the incomplete body.

Required change: emit and test the full documented `update` parameters after
choosing the intended fetch-and-merge behavior, and validate generated operation
bodies against the pinned API contract before re-review.

Official basis: [Create a repository ruleset](https://docs.github.com/en/enterprise-cloud@latest/rest/repos/rules#create-a-repository-ruleset).

### P1 F-02: the owner can also be admitted as the broker and bypass confinement

`github_target_policy.py:75-92` validates a broker in isolation, lines 169-175
never require the broker user id to differ from the owner, and lines 155-156
grant the owner user id an `always` bypass. GitHub keys a `User` bypass actor to
that actor id. A broker token with restricted repository permissions does not
change the actor's user id.

An independent deterministic probe supplied the same user id for owner and
broker. The comparator returned `ready_for_review` with two ruleset POSTs while
the non-dev bypass actor id was exactly the broker id. This defeats
`non_dev_update_restriction` for the admitted broker and contradicts the task
record's statement that the observed owner/admin account is not an admissible
restricted broker principal.

Required change: reject owner/broker identity aliasing by immutable user id
(with login consistency also checked), and add same-id/different-case and
same-object adversarial tests.

Official basis: [Ruleset bypass actors and update rule](https://docs.github.com/en/enterprise-cloud@latest/rest/repos/rules#create-a-repository-ruleset).

### P1 F-03: workflow source identity is recorded but not bound to the accepted check

`github_target_policy.py:95-109` records an exact workflow path, source ref, and
source commit, but lines 137-143 enforce only a check context and GitHub App id.
GitHub documents that required status checks do not distinguish workflow,
matrix, or event trigger type. The existing observation path compounds the gap:
`github_checks.py:53-63` accepts any syntactically valid workflow path, and its
normalized check at lines 79-81 retains the run head SHA but not the path.

Consequently a different workflow under the same app that emits the same job
name can satisfy both the destination rule and the local check observation. The
policy's `source_commit` and `path` are digest-bound metadata, not predicates on
the accepted run. The tests mutate the self-reported workflow object but do not
exercise a same-app/same-name run from another valid workflow path.

Required change: bind the actual run to the reviewed workflow path and source
identity throughout policy, PR plan, observation, and decision, or use and
qualify GitHub's workflow ruleset primitive where available. Add collision tests
for another workflow with the same app and job/check name.

Official basis: [Troubleshooting rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/troubleshooting-rules#troubleshooting-required-status-checks) and [repository ruleset workflow parameters](https://docs.github.com/en/enterprise-cloud@latest/rest/repos/rules#create-a-repository-ruleset).

### P2 F-04: complete effective-policy visibility is asserted, not digest-bound

`github_target_policy.py:234-275` carries only four visibility booleans and the
normalized repository rulesets. It has no repository id, effective-rule bodies,
or classic branch-protection state. Lines 289-308 trust a `true` boolean and
compare only normalized rulesets. GitHub documents that rulesets aggregate with
classic branch protection; those effective constraints can change operation
behavior even when the represented ruleset list is unchanged.

The refresh narrative records repository id and a `dev` protection 404, but
`current-target-policy-2026-09-22.json` drops both before computing its
observation digest. A recreated/transferred same-name repository or changed
classic protection can therefore leave the canonical observation and plan
digests unchanged. The tests only flip completeness booleans and do not prove
that the claimed complete state is present in the digest.

Required change: bind immutable repository identity and all effective policy
inputs, including classic protection or an explicit verified-absent record, in
the observation and drift comparison. A visibility assertion without the
corresponding bounded records must not unlock operation materialization.

Official basis: [About rule layering](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets#about-rule-layering).

## Verified Guarantees

- Current unresolved evidence reproduces exactly and remains blocked with zero
  operations and `apply_authorized: false`.
- Exact raw file hashes in `target-policy-source-checkpoint.md` match.
- Canonical policy, observation, and plan digests recompute exactly as
  `db1b1ad6e96d287386ad5d99c600b938c3e65dc12123a98954106d58bab68b7f`,
  `907688c5defff9615e8f8d5f0bac9d9e39e8d3bf6522ceb7f2813c51df134798`,
  and `5c243ac74ff1deff1780debe97e5e0ec1dcfa42653d2898c37db84b54ef15d7d`.
- Exact-field checks, bounded text, positive integer identities, 16-record
  ruleset ceiling, depth/node/byte limits, and deterministic sorted operation
  order provide useful local boundedness.
- The policy module imports only local validation/canonicalization helpers and
  `re`. It constructs PATCH/POST descriptions as data but contains no HTTP
  client, filesystem writer, credential reader, sender, dispatcher, retry, or
  apply entry point. No production module imports it at this checkpoint.
- The restricted permission map rejects administration/workflow write access,
  but the real broker principal and the evidence proving its effective token and
  repository permissions remain unresolved external prerequisites.

## Local Verification

- PASS: `py -3 -B .aide/scripts/tests/test_continuous_worker_github_observation.py -v`
  ran 44 tests in 0.136 seconds.
- PASS: `py -3 -B .aide/scripts/tests/test_continuous_worker_github_http.py -v`
  ran 19 tests in 1.342 seconds.
- PASS: `py -3 -B .aide/scripts/tests/test_continuous_worker_provider_bridge.py -v`
  ran 12 tests in 93.233 seconds.
- PASS WITH ONE RETAINED HOST GAP:
  `py -3 -B .aide/scripts/tests/test_continuous_worker_integration_broker.py -v`
  ran 37 tests in 174.855 seconds; 36 passed and the disposable-symlink case
  skipped because this Windows identity lacks symlink privilege.
- PASS: independent same-owner/broker probe reproduced F-02 and also showed the
  generated `update` rule is exactly `{"type":"update"}`.
- PASS: source/evidence SHA-256 and canonical digest recomputation.
- PASS: `git diff --check` for `base..source` and the review worktree.

Passing local tests do not discharge the findings: no test validates the
generated ruleset body against the pinned REST schema, rejects owner/broker
aliasing, binds an actual run to the reviewed workflow path, or includes the
effective policy state in the canonical observation.

## Retained Blockers

- Exact restricted broker principal and workflow/check identities are unresolved.
- The current target has no recorded installed workflow or qualifying rulesets.
- Settings/workflow installation, hosted adversarial races, protected-host/store
  qualification, and isolated-host close dependency remain unrun.
- Source defects F-01 through F-04 require remediation and a new exact-source
  independent review before any target operation can be considered.
- The task must remain `needs_review`; this review does not authorize mutation.
