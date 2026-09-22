# GitHub Target-Policy Independent Review

Review date: 2026-09-22

## Superseding Outcome

`REQUEST_CHANGES`

This rereview supersedes the verdict for the repaired exact commit without
erasing the initial `REQUEST_CHANGES` history. F-01, F-02, and F-04 are closed.
F-03 remains materially open: the generated `workflows` rule has the documented
field shape, but GitHub documents ruleset workflows as organization- or
enterprise-level controls, while the exact target is the user-owned repository
`Julesc013/aide`. The represented workflow event is also `push`, while GitHub
requires a ruleset workflow file to include `pull_request`,
`pull_request_target`, or `merge_group`.

The current unresolved packet remains fail-closed with zero operations. This
review does not authorize target mutation, workflow or ruleset installation,
credential or principal creation, settings changes, branch changes, push,
merge, tag, release, or any other hosted effect.

## Exact Review Subject

- Repaired published commit: `9383c2b5e8521bbdf9d0a54648459ee25d76c1b3`.
- Repaired tree: `572b2f4f8bbbcf896b4c1661157658b6907c37c6`.
- Exact parent and initial-review commit:
  `9bba1cecaec835b5299cf02718059a94ef4c08cb`.
- Local `HEAD` and `origin/task/aide-cw-github-target-qualification-01` both
  resolved to the repaired commit at review start.
- The exact parent-to-repair diff contains 10 paths, all within the task's
  declared allowed paths. `git diff --check` passes.

Reviewed source identities:

- `core/runtime/integration_broker/github_target_policy.py`: Git blob
  `bd9907be0da7fa442d4498e8a047221eb9a6d3df`; SHA-256
  `75e61dbb5ce4f085b885da08616f9a19bf667ae1d4c50cfd834ecbf21fcca2d2`.
- `.aide/scripts/tests/test_continuous_worker_github_observation.py`: Git blob
  `0ade7c372ad0dd66e940380e7d2e4f7f2d9168ce`; SHA-256
  `3ff68a757329e91564b8e69adf7a3b47d13d208d91973eaaf4fd0dda18860236`.

## Superseding Finding

### P1 F-03: the replacement workflow control is not qualified for this target

`github_target_policy.py:148-159` adds a `workflows` rule to a repository-level
`POST /repos/Julesc013/aide/rulesets`. Its `path`, `repository_id`, `ref`, and
`sha` fields match the generic REST request schema. That schema is not enough to
establish target applicability: GitHub's current ruleset documentation states
that ruleset workflows are configured at the organization or enterprise level.
The reviewed target observation identifies `Julesc013` as a `User`, not an
organization, so this repository-level operation has no documented supported
deployment path for the exact target.

There is a second unresolved premise in the same repair. The policy requires
the workflow identity's event to be `push` at lines 96-111. GitHub documents
only `pull_request`, `pull_request_target`, and `merge_group` as supported
ruleset-workflow events, and says at least one must appear in the workflow
file. The packet has no installed workflow and no source-file evidence proving
one of those supported triggers. Consequently the new
`exact_required_workflow` destination guarantee is not established, and the
original same-app/same-name collision risk remains unresolved for the only
documented, target-applicable required-status-check mechanism.

Required change: either bind the actual accepted run to the reviewed workflow
path/source throughout the local plan, observation, and decision contract, or
replace the proposed control with an officially documented mechanism that is
available for this user-owned repository. If a ruleset workflow remains part of
the design, its supported target level and event trigger must be represented
and independently qualified before an exact operation can be review-ready.

Official basis:

- [GitHub REST API 2026-03-10 versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions).
- [Create a repository ruleset](https://docs.github.com/en/enterprise-cloud@latest/rest/repos/rules#create-a-repository-ruleset).
- [Available rules: require workflows](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-workflows-to-pass-before-merging).
- [Troubleshooting ruleset workflows](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/troubleshooting-rules#troubleshooting-ruleset-workflows).

## Finding Closure Matrix

- `F-01 CLOSED`: the non-dev update rule now emits
  `parameters.update_allows_fetch_and_merge: false`, which the pinned
  `2026-03-10` REST schema requires. The focused test and independent probe
  assert the exact body.
- `F-02 CLOSED`: policy construction and validation reject broker/owner
  equality by immutable user id or case-insensitive login. Independent probes
  confirmed both refusal paths.
- `F-03 OPEN`: the source-binding fields are present, but the replacement
  control is not documented for a user-owned repository and the represented
  `push` event does not satisfy ruleset-workflow trigger requirements.
- `F-04 CLOSED`: repository id, bounded effective-rule records, and explicit
  classic branch-protection state are required observation fields, enter the
  canonical digest, and block operation materialization on drift. Hosted
  non-empty normalization remains an external qualification step.

## Canonical Evidence

Exact raw SHA-256 values:

- Desired policy: `245a8d871301b255d9cbc0abfa3e7fde2e8ccfea0e7f0b88e01ebcbe149e8146`.
- Current observation: `020650ae5932c672313248a4be57011b1e75046fed19e0c15e99cad095f9f75b`.
- Review plan: `a0aec7f8c4db5191167a662bbc2ca66a742c2ed498f80cfd2e1ea9a36c95773c`.
- Repair record: `9a28d24193c115c90abaca03b0375208d73e4bd04ebc0d46c974314b1f6333f6`.
- Source checkpoint: `a5cebfe61f0939a2b72bbc8dc5dd1d3194639000b0285104a839bf68f6d78ed9`.
- Validation record: `7e5ec1db098ad4c5977b38ca8ea40c5cafc9b06aef2291ae8dc819dd1c58dd93`.

Canonical recomputation reproduced:

- Policy digest: `0c3c1ce858c4e70e0070074f66db31873c7a1f4b9aa820066f760678ed35ba89`.
- Observation digest: `a1261592a0d53ac3ded981a19e32b0b323f085da45cf041893c76078b767c86a`.
- Plan digest: `762da6e0de4359fcc1316529e9f715f075bac0e37f42e7a9ec2127f3b5469336`.
- Desired policy and review plan regenerate data-exactly from the pure builder
  and current observation.
- Current plan status is `blocked` on `broker_principal_unresolved` and
  `workflow_check_identity_unresolved`; it has zero operations and
  `apply_authorized: false`.

## Verified Guarantees

- Exact-field validation, bounded strings and positive identifiers, a 16-record
  repository-ruleset ceiling, a 128-record effective-rule ceiling, and
  depth/node/byte limits keep the pure comparison bounded.
- Repository identity, observer/admin identity, complete-visibility flags,
  principal permissions, workflow identity, repository rulesets, effective
  rules, classic protection, and repository settings are digest-bound.
- Drift in repository id, effective rules, or classic protection changes both
  observation and plan digests and yields a blocker with no operations.
- The permission contract excludes administration and workflow write access;
  GitHub requires Administration write permission to create a repository
  ruleset, so policy installation is necessarily outside the broker identity.
  The real restricted broker and its effective permissions remain unresolved.
- The target-policy module imports only local validation/canonicalization
  helpers and `re`. It has no HTTP client, credential reader, filesystem writer,
  sender, retry, dispatcher, or apply entry point, and no production module
  imports it at this checkpoint.
- The repair adds no `.github/workflows` file and no apply, network, or
  credential path. No GitHub target, Git ref, index entry, commit, branch, tag,
  or object database was mutated during rereview.

## Local Verification

- PASS: `py -3 -B .aide/scripts/tests/test_continuous_worker_github_observation.py -v`
  ran 46 tests in 0.129 seconds.
- PASS: `py -3 -B .aide/scripts/tests/test_continuous_worker_pr_observation.py -v`
  ran 21 tests in 65.303 seconds.
- PASS: `py -3 -B .aide/scripts/tests/test_continuous_worker_github_http.py -v`
  ran 19 tests in 1.156 seconds.
- PASS: `py -3 -B .aide/scripts/tests/test_continuous_worker_provider_bridge.py -v`
  ran 12 tests in 80.727 seconds.
- PASS WITH ONE RETAINED HOST GAP:
  `py -3 -B .aide/scripts/tests/test_continuous_worker_integration_broker.py -v`
  ran 37 tests in 158.111 seconds; 36 passed and the disposable-symlink case
  skipped because this Windows token lacks symlink privilege.
- PASS: 135 total affected cases, 134 passed, one skipped, zero failures.
- PASS: independent probes confirmed the complete update rule, same-id and
  case-folded-login refusal, exact emitted workflow fields, and digest/blocker
  changes for repository-id, effective-rule, and classic-protection drift.
- PASS: exact evidence regeneration, raw SHA-256 recomputation, source Git blob
  checks, `git diff --check`, changed-path scope, and static absence-of-effect
  scans.

All tests and probes were local and deterministic. No credential-dependent or
GitHub API operation was run.

## Retained Blockers

- F-03 requires a target-applicable workflow-source binding before the resolved
  operation packet can be accepted.
- Exact restricted broker principal and effective repository permissions remain
  unresolved.
- Exact workflow/check identity and a supported workflow trigger remain
  unresolved; the target has no recorded installed workflow or qualifying
  rulesets.
- Settings/workflow installation, hosted adversarial races, non-empty effective
  policy normalization, protected-host/store qualification, and the
  isolated-host close dependency remain unrun.
- The task remains `needs_review`; no target mutation is authorized.

## Initial Review History

The initial review remains an auditable part of this file:

- Verdict: `REQUEST_CHANGES`.
- Source: `bb433bb74f645e0904ca34bf3af38516ae05a7ad`, tree
  `a871c65880161f147f35cf8df7269bba9af3a867`.
- Published head: `eb4dea3f30ab53e3e57fe85eae97fa07de6e414c`, tree
  `41adc996349690b4d796d8005ef179c89fb93c8e`.
- Review commit: `9bba1cecaec835b5299cf02718059a94ef4c08cb`.
- Initial Markdown blob/SHA-256:
  `7103255f96461b1b1edc88dbc7b6bdd4e40e10cb` /
  `e69a8b86a6f6de5040d2ebdc8d60855006c420283dd7ce407cb904f9f004d915`.
- Initial JSON blob/SHA-256:
  `6a52271d2ec4727a0851156da57b3cb6ecbb0d00` /
  `dec5691bc4c0f59338f2b35f4b48052356e123fa3c06f9444d3b34a16014dfce`.
- Initial F-01 (P1): generated update rule omitted required API parameters.
- Initial F-02 (P1): owner and broker could resolve to the same bypass actor.
- Initial F-03 (P1): reviewed workflow source was not bound to the accepted
  required check.
- Initial F-04 (P2): canonical observation omitted effective-policy inputs.

The initial review ran 44 focused tests, 19 bounded HTTP tests, 12 provider
bridge tests, and 37 integration-broker tests with the same one symlink skip;
its same-owner probe reproduced F-02. Its request for changes is historical
fact even though three findings are closed by the repaired commit.
