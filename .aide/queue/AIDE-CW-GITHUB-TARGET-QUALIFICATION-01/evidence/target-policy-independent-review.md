# GitHub Target-Policy Independent Review

Review date: 2026-09-22

## Superseding Outcome

`REQUEST_CHANGES`

This third review supersedes the verdict for exact follow-up commit
`cb05b135eb0d9012e3d40e37a195f65abbab0b7a` without erasing either prior
`REQUEST_CHANGES` round. The repair removes the unavailable required-workflow
operation from the user-owned target, classifies destination, local, monitored,
and unsupported guarantees truthfully, rejects same-app/name substitution, and
binds its synthetic accepted provenance through the plan, raw observation,
durable decision/intent, and registered bridge.

F-03 nevertheless remains open. The collector rejects the workflow-run `path`
representation shown by GitHub's 2026-03-10 documentation
(`.github/workflows/file.yml@ref`)
because it compares that raw value to a plan field that permits only the bare
path. The committed bare-only fixture does not exercise that documented API
response shape, so all local tests pass without covering it.
This is fail-closed, but it prevents a documented real workflow run from
reaching the durable qualification chain and therefore does not complete target
qualification.

The current unresolved packet remains blocked with zero operations. This review
does not authorize target mutation, workflow or ruleset installation, credential
or principal creation, settings changes, branch changes, push, merge, tag,
release, or any other hosted effect.

## Exact Review Subject

- Follow-up commit: `cb05b135eb0d9012e3d40e37a195f65abbab0b7a`.
- Tree: `48582b5476afc88eb72a5b1dd343495017e402f4`.
- Parent: `9383c2b5e8521bbdf9d0a54648459ee25d76c1b3`.
- Branch: `task/aide-cw-github-target-qualification-01`.
- Local `HEAD` and its local remote-tracking ref both resolved to the exact
  follow-up commit at review start.
- The exact parent-to-follow-up diff contains 18 paths and passes
  `git diff --check`.
- Two changed test paths are outside `task.yaml`'s declared `allowed_paths`:
  `.aide/scripts/tests/test_continuous_worker_pr_observation.py` and
  `.aide/scripts/tests/test_continuous_worker_provider_bridge.py`.

Reviewed source identities:

- `github_target_policy.py`: blob
  `b7ee5c19c4bc95f90aeb16e25a34bfb04386d8b4`; SHA-256
  `ed2d5e6ae5a03c3e53e5e019ca972c67132367ec404807bb6dc035b515e37bd6`.
- `github_checks.py`: blob `2433e901212d974003a297f9ffacfad5299dc175`;
  SHA-256 `e13c1e2a77ad214d8edadfba9a2369cfa0f883cba526d5301db2ad77e3dcef05`.
- `pr_observation.py`: blob `2c8f6dc2ebe78314af05a5e8dbca63b5007bf4bb`;
  SHA-256 `ac37b9990a1c8b92e3285a77195c77968614407d9c99147e8dc191372d5c2e39`.
- Focused observation test: blob
  `bb7e4cc860cf58aab9b911235a8f6c4cb5eb1a4e`; SHA-256
  `40ff3189bcbabd1a021dda0e1784fa67deed4d00c6d2758c148ba49e4b480201`.
- PR observation test: blob `028586d3137929bac0b53665bf1c9e073c2c3e03`;
  SHA-256 `6b35b1b3dffe501cdd0f840abaf9fc6e0ef0c336623724f7e4a6dcecb4cc5ece`.
- Provider bridge test: blob `b2b7cfb7b470a929aa05a23b8f38e1f903f1d075`;
  SHA-256 `7cf1e4c67bf9b4e17d0cae8113f5eaa15ff91f39af5cf2d9a3f55145ae815ac5`.

## Findings

### P1 F-03: documented workflow-run paths cannot enter qualification

At `github_checks.py:53-57`, the collector accepts an optional `@ref` in its
regular expression but then requires the entire raw value to equal the bare
planned path. At `pr_observation.py:34-40` and `pr_observation.py:89-108`, both
the plan and normalized observation permit only a bare path. The test fixture at
`test_continuous_worker_github_observation.py:118-124` likewise supplies only a
bare path.

GitHub's current workflow-run REST documentation, with
`X-GitHub-Api-Version: 2026-03-10`, shows `path` as
`.github/workflows/build.yml@main` for a workflow-run attempt. The exact
versioned OpenAPI component marks `path` required and uses
`octocat/octo-repo/.github/workflows/ci.yml@main` as its example. Independent
API-faithful probes changed only the fixture path to
`.github/workflows/aide-cw-checks.yml@task/aide-cw-...`; the collector refused
it as a workflow-source mismatch and likewise refused the repository-prefixed
OpenAPI example shape. Same-app/name substitution to a different path and the
same path with a wrong ref were also refused, which is correct, but the
documented legitimate shapes are indistinguishable from an invalid source under
the current contract.

Impact: the implementation fails closed before it can accept and durably bind a
GitHub Actions run having the documented shape. Passing fixtures therefore do
not establish the claimed local workflow-source qualification for that API
shape.

Required change: parse and validate the documented `path@ref` representation,
bind the entry path and its source selector to the admitted branch/head semantics,
and retain the accepted representation or an unambiguous normalized path/ref pair
through the normalized observation, durable decision/intent, and bridge. Add an
official-shape positive fixture plus wrong-path, wrong-ref, missing-ref, and
malformed-ref refusals.

Official basis:

- [REST API endpoints for workflow runs](https://docs.github.com/en/rest/actions/workflow-runs).
- [GitHub REST OpenAPI description 2026-03-10](https://github.com/github/rest-api-description/blob/main/descriptions/api.github.com/api.github.com.2026-03-10.json).
- [REST API endpoints for workflow jobs](https://docs.github.com/en/rest/actions/workflow-jobs).
- [REST API endpoints for check runs](https://docs.github.com/en/rest/checks/runs).
- [Troubleshooting required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

### P2 S-01: the follow-up diff exceeds the declared task paths

The follow-up changes the PR-observation and provider-bridge tests, while
`task.yaml:18-27` allows only the focused GitHub-observation test under
`.aide/scripts/tests/`. These tests are relevant to the requested end-to-end
binding, but the canonical task record was not expanded before the changes.

Required change: route any scope expansion through the canonical queue record
and its review gate. This review does not authorize such an edit.

## F-03 Closure Matrix

- `CLOSED`: the user-owned target emits no `workflows` rule or required-workflow
  endpoint. A resolved synthetic plan contains one repository settings `PATCH`
  and two repository ruleset `POST`s only.
- `CLOSED`: destination-enforced guarantees are limited to expected-head,
  app-bound status check, PR-only dev updates, non-dev update restriction,
  deletion restriction, and non-fast-forward restriction.
- `CLOSED`: exact workflow run path/event/head is classified as a local
  precondition; run/attempt and check-run/suite identities are monitored;
  server exact-source enforcement and same-app/name collision exclusion are
  explicitly unsupported.
- `CLOSED`: same-app/name substitution, missing run/check/suite identities, and
  malformed normalized identities refuse. Malformed observations create no
  durable mutation intent, and unresolved target identity yields zero review
  operations.
- `CLOSED FOR THE SYNTHETIC SHAPE`: workflow path/event/head, workflow run id and
  attempt, check run id, and check suite id survive normalized observation,
  decision validation, SQLite observation storage, intent digest, staged
  transport, and registered-bridge observation-digest checks.
- `OPEN`: the synthetic accepted bare path is not the documented workflow-run
  `path@ref` shape, so the chain is not qualified for official API input.

## Canonical Evidence

Exact raw SHA-256 values:

- Desired policy: `c516b0e8f655870dd3123ce6a175a2108dbe76a8d8a4e4cfda7be90fbfb05ff9`.
- Current observation: `020650ae5932c672313248a4be57011b1e75046fed19e0c15e99cad095f9f75b`.
- Review plan: `54a18d662e6bc397eba1d6ae7dd66c99a29e42e47a1dfd8b741e0165590d7bbb`.
- Repair record: `af61938768eabd5b08f87cdabdc374a7f62609c1acc7433cbfed50b06cfbeff6`.
- Source checkpoint: `51f171fde3f0b2824bd7e0aea62e2c8c7f65c951b8f990b4b059c2f0a8344f66`.
- Validation record: `346abab087a543719d2528f51c2d2eeb5f3bbd5923d69f82986292c16c1e998a`.
- Remaining risks: `a7e62dd73d9ecfb2ced8596c8241399c9bbcf5d30cf640f2a0e109a0ed74711b`.

Canonical recomputation reproduced:

- Policy digest: `c79b62b9fc888aa50600334e3b7108addc91f543b4ea7e3e4505d0a8aef636c9`.
- Observation digest: `a1261592a0d53ac3ded981a19e32b0b323f085da45cf041893c76078b767c86a`.
- Plan digest: `a754af93595c26612edc13d52456e0d7ef64b07120e639001a05a91b1b3d3655`.
- Desired policy and review plan regenerate data-exactly from the pure builder
  and current observation.
- Current status is `blocked` on `broker_principal_unresolved` and
  `workflow_check_identity_unresolved`; operation count is zero and
  `apply_authorized` is false.

## Local Verification

- PASS: focused GitHub observation suite, 46 tests in 0.093 seconds.
- PASS: PR observation suite, 21 tests in 62.477 seconds.
- PASS: bounded GitHub HTTP suite, 19 tests in 1.089 seconds.
- PASS: provider bridge suite, 12 tests in 88.302 seconds.
- PASS WITH ONE RETAINED HOST GAP: integration-broker suite, 37 tests in
  181.390 seconds; one disposable-symlink case skipped for unavailable Windows
  symlink privilege.
- PASS: 135 total affected cases, 134 passed, one skipped, zero failures.
- PASS: independent probes refused same-app/name source substitution, missing
  run/check/suite identities, and missing normalized identities; confirmed no
  required-workflow operation and zero operations for unresolved target identity.
- PASS: the durable probe retained all provenance identities and bound the
  `merge` intent to the exact observation digest.
- EXPECTED REFUSAL / FINDING REPRODUCED: relative `path@ref` and
  repository-prefixed OpenAPI example-shape probes were refused as
  workflow-source mismatches; a wrong-ref probe also refused.
- PASS: exact regeneration, raw SHA-256 and Git blob recomputation,
  `git diff --check`, and static no-effect scans.

The initial dotted-module `unittest` invocation failed with
`ValueError: Empty module name` because `.aide` is not an importable dotted
package name; the same five suites were rerun successfully with deterministic
`unittest discover` file patterns. All tests and probes were local. Official
documentation was read over HTTPS, but no GitHub REST API or credential-dependent
operation was executed.

## Retained Blockers

- F-03 needs an official-response-shape workflow path/ref contract and tests.
- Exact restricted broker principal and effective repository permissions remain
  unresolved.
- Exact target workflow/check identity remains unresolved; the target has no
  recorded installed workflow or qualifying rulesets.
- Settings/workflow installation, hosted adversarial races, non-empty effective
  policy normalization, protected-host/store qualification, and the isolated-host
  close dependency remain unrun.
- The two out-of-scope test changes require canonical scope disposition.
- The task remains `needs_review`; no target mutation is authorized.

## Prior REQUEST_CHANGES History

### Round 1: Initial Review

- Verdict: `REQUEST_CHANGES`.
- Source: `bb433bb74f645e0904ca34bf3af38516ae05a7ad`, tree
  `a871c65880161f147f35cf8df7269bba9af3a867`.
- Published head: `eb4dea3f30ab53e3e57fe85eae97fa07de6e414c`, tree
  `41adc996349690b4d796d8005ef179c89fb93c8e`.
- Review commit: `9bba1cecaec835b5299cf02718059a94ef4c08cb`.
- Markdown blob/SHA-256: `7103255f96461b1b1edc88dbc7b6bdd4e40e10cb` /
  `e69a8b86a6f6de5040d2ebdc8d60855006c420283dd7ce407cb904f9f004d915`.
- JSON blob/SHA-256: `6a52271d2ec4727a0851156da57b3cb6ecbb0d00` /
  `dec5691bc4c0f59338f2b35f4b48052356e123fa3c06f9444d3b34a16014dfce`.
- Findings: F-01 missing update parameters; F-02 owner/broker aliasing;
  F-03 unbound workflow source; F-04 omitted effective-policy inputs.

### Round 2: First Repair Rereview

- Verdict: `REQUEST_CHANGES`.
- Source: `9383c2b5e8521bbdf9d0a54648459ee25d76c1b3`, tree
  `572b2f4f8bbbcf896b4c1661157658b6907c37c6`.
- Parent review commit: `9bba1cecaec835b5299cf02718059a94ef4c08cb`.
- Markdown blob/SHA-256 at the follow-up review boundary:
  `542dd632700f291ab98a48cd20bd4b5b582c5fc8` /
  `be9da84f70698a5d34e392f8328d8a0049ce556ffcad243da0a9fdabeb469a87`.
- JSON blob/SHA-256 at the follow-up review boundary:
  `a6756731bdc003bd44adb1222cdb81174b712fff` /
  `d1961d3fe29ca497d22dfed3185735e7a99e64cbfa5c850b804103313cf23485`.
- F-01, F-02, and F-04 closed. F-03 remained open because the proposed
  required-workflow ruleset operation was unavailable for the user-owned target
  and its represented `push` trigger did not meet that control's requirements.

No prior finding or verdict is erased by this superseding record.
