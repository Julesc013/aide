# Expected-Head Merge Source Review

Date: 2026-09-22

## Primary contract

GitHub documents the synchronous endpoint as
`PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge`. Its request body accepts
`sha`, described as the SHA that the pull request head must match, and
`merge_method`. A head mismatch returns HTTP 409. The endpoint does not expose
an expected base SHA or expected base-ref argument.

Source: [GitHub REST API - Merge a pull request](https://docs.github.com/en/enterprise-cloud@latest/rest/pulls/pulls#merge-a-pull-request).

## Implemented classification

- Destination-enforced by this request: candidate head SHA.
- Fixed request choice: synchronous endpoint and ordinary `merge` method.
- Rechecked locally before construction: repository, pull identity, base SHA and
  ref, head SHA and ref, author, required checks, policy digest and merge-contract
  digest.
- Not established as endpoint-atomic: base SHA/ref, actor, policy, ruleset,
  bypass state, principal permissions and target-ref update denial.
- Successful response meaning: submitted acknowledgement only.
- Integration meaning: reserved for a later authenticated exact observation.

## Scope and gates

`github_merge.py` is a pure request builder and response classifier. It contains
no token handling, HTTP sender, retry loop, settings mutation, workflow install,
branch mutation or factory reachable from the production worker. The existing
durable bridge remains responsible for one mutation intent and observe-only
uncertain recovery. Hosted enforcement remains unrun and unclaimed.

## Exact source identities

- `core/runtime/integration_broker/github_merge.py` SHA-256:
  `efd3be08f4be387d45f20d53df75b00c8df4413d532c9bead271a9f8168ab3fc`.
- `.aide/scripts/tests/test_continuous_worker_github_observation.py` SHA-256:
  `5e1e2216d8a298909039b8424fcc714c97bb5fdd324a622c8b79ae693de97ad1`.

The identities bind the reviewed working-tree bytes before commit. The eventual
commit identity additionally binds their repository context.
