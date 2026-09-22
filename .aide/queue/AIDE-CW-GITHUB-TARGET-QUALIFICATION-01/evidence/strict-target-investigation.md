# Conditional GitHub exact-base contract investigation

Observed documentation date: 2026-09-07. This is a source-backed design and
local graph experiment plan, not hosted qualification or installed policy.

## Documented server mechanisms

GitHub's strict required checks require the topic branch to include current
base-branch work before merging. Administrators normally bypass classic branch
protection unless enforcement includes them. An actual named required check is
necessary; a strict checkbox with no required check does not establish the
contract. Required checks can be constrained to an app. GitHub accepts skipped
and neutral as well as successful conclusions, so our required workflow must
have a non-skippable final gate and authenticated provenance.
[Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches),
[Creating rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository).

The synchronous REST merge endpoint accepts an expected head SHA and returns
409 for a mismatch. Its arguments do not include an expected base SHA or base
ref. Updating a PR can change its base. The initial implementation will use
this synchronous endpoint with an explicit head and merge method; asynchronous
merge admission and automatic retries are distinct operations and are excluded.
[Pull request REST API](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request).

Ordinary GitHub merge commits use no-fast-forward merging. GitHub can also mark
a PR merged indirectly when its commits reach the base by another path, even
if that PR's protections were not satisfied. A merged flag alone therefore
proves neither broker authority nor the required merge parents/checks.
[Pull request merges](https://docs.github.com/en/pull-requests/reference/pull-request-merges).

Rulesets can independently deny updates, deletion and non-fast-forward history
changes, with actor-specific bypass. Effective active rules and their complete
bypass visibility must be observed. A hidden bypass list is unknown. Classic
branch push restrictions are limited to organization-owned repositories, so the
personal-repository proposal must investigate supported rulesets instead of
assuming those classic restrictions exist.
[Available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets),
[Rules REST API](https://docs.github.com/en/rest/repos/rules),
[Branch protection REST API](https://docs.github.com/en/rest/branches/branch-protection).

GitHub chooses the workflow version associated with the triggering event's
commit/ref. A restricted push-event contract can use authenticated run/ref/head
provenance to derive that source version; the normalizer must not copy the
planned workflow SHA into observed facts. Pull-request merge refs, reusable
workflows and reruns need their own exact provenance checks or must refuse.
[Workflow execution](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows).

## Inference and proof obligations

Let B be the admitted base and C the literal candidate with exactly one parent
B. A monotonic target T after observation satisfies B <= T. Strict server
up-to-date enforcement requires T <= C. Because C has no intermediate parent
commit, T must equal B or C. For a new nontrivial merge, C is not already in T,
so T must be B. Thus a forward competing target commit cannot silently change
the merge base. Expected-head matching prevents substituting an updated topic
branch. This is an inference from Git ancestry and documented prerequisites,
not a GitHub promise of a general expected-base API.

The T=C case must produce no new merge and cannot be accepted from a merged
boolean alone. Immutable ordered merge parents [B,C], exact tree, target
ancestry, required successful checks and the durable merge intent remain
necessary before this broker records integration.

Strict checks alone do not bind the target ref. An authorized writer could
retarget the PR from dev to main at the same B between observation and merge.
Expected-head C and strict checks still hold. The concrete remedy is a broker
principal with server-enforced update denial on every non-dev branch, including
branches created after qualification. Its immutable task branches may be created
once but never updated. Preserve owner access with a separately identified
owner bypass that does not include the broker. This requires actual principal
and ruleset qualification before apply, not a caller-supplied permission flag.

Policy must remain enforced during dispatch. Administrative policy changes are
controlled operator actions and invalidate the finite qualification. The broker
must have no policy-write/bypass capability; an arbitrary settings administrator
is outside this contract's trust boundary. Ref/history deletion, rollback,
unknown policy visibility and unexpected actor permissions refuse.

## Required experiments and current limits

The adjacent local script uses real disposable Git commits/trees and explicit
read-then-dispatch barriers. It tests the conditional graph proof and constructs
counterexamples when strict checking, monotonic history, expected head, single
parent or non-dev update denial is absent. The script models the documented
server predicates; passing it does not show that GitHub actually enforces them.

The target ExecPlan requires corresponding hosted experiments with exact raw
requests/responses and immutable post-effect objects after independent review
of the actual configuration. Current broker principal, effective rules, hosted
workflow and source provenance remain unresolved. No target or credential
setting has been modified.
