# Exact GitHub broker target contract

The implementation starts from reviewed broker checkpoint 8c3df653. This planned
item owns actual target policy and hosted acceptance, not another broker
foundation. No settings or credentials have changed through its admission.

1. Observe the current repository, effective branch protection/rulesets, bypass
   visibility, allowed merge methods, required checks, actual workflow sources
   and broker principal capabilities. Use the approved real Windows/GitHub user
   context for credential-dependent observations. Record exact raw bytes; a
   hidden bypass list is unknown, never an empty list. Identify whether the
   current repository plan supports the proposed rules.
2. Produce exact non-mutating desired/current policy JSON and a scoped apply
   plan preserving existing owner operations. The strict dev policy requires
   a real named check from the approved app, up-to-date branches, no bypass,
   no force push or deletion, and ordinary merge commits. A separate active
   rule must deny the broker principal updates to every non-dev ref, including
   later-created refs; its request branches are created once and never updated.
   This prevents a same-OID PR retarget race. Resolve the actual principal and
   non-dev owner bypass IDs; unresolved IDs make apply unavailable.
3. Add actual hosted workflow/check provenance for the frozen candidate, with
   explicit failure propagation and no skipped/neutral success shortcut. Select
   and pin real action/tool versions through target GitHub advisory/validate.
   The provider cannot fabricate workflow_sha from the desired plan or merely
   trust a self-reported workflow artifact. Restrict the first contract to an
   event whose authenticated run/ref/commit determines its source version.
4. Implement policy validation and the fixed expected-head merge request. Use
   the synchronous endpoint and ordinary merge method initially; queue/async
   retries are outside this finite contract. No refresh/rebase changes a frozen
   candidate. Keep all stage intents and observe-only uncertain recovery.
5. Independent review must bind exact policy/workflow/principal/apply-plan bytes
   before any settings installation. Then apply only the reviewed target item
   and observe the effective result. No inferred global setting changes.
6. On a separately identified disposable hosted target, run deterministic
   barriers: advance base after final read, change head, retarget to another
   same-OID base, roll back or delete/recreate the base, loosen policy/bypass,
   alter checks, and lose the successful merge response. Require server refusal
   and unchanged protected refs where an effect was inadmissible. Test target
   already equal to/descended from candidate without creating another merge.
7. Bind server request IDs/statuses, current policy/actor, exact merge objects
   and source hashes to a finite qualification receipt. Current target acceptance
   additionally needs protected host/store qualification. Revalidate before
   actual two-task pilot use; the broker remains incomplete until then.

The conditional graph proof is narrow: for candidate C with sole parent B,
monotonic target B <= T and strict server condition T <= C imply T is B or C.
A new nontrivial merge therefore starts at B; C is already integrated. The proof
assumes policy remains enforced and the operation cannot retarget. Local graph
fixtures can disprove missing premises but cannot verify GitHub enforcement.

Start: policy/source preparation has no broker-completion dependency. Close:
this item requires actual hosted contract acceptance and isolated-host binding.
Full broker closure depends on this receipt; the item does not depend on full
broker closure, avoiding a circular completion gate.

## Progress - 2026-09-22 expected-head source slice

- [x] Reconfirm the documented synchronous merge endpoint and its expected-head
  `sha` predicate.
- [x] Implement a pure fixed request/response contract with no installed sender,
  credential source, settings mutation or retry path.
- [x] Revalidate the exact current base, head, actor, checks, policy digest and
  merge-contract digest before request construction.
- [x] Keep a successful synchronous response at `submitted`; only a later
  authenticated observation may establish `integrated`.
- [x] Pass 31 focused observation/merge-contract tests.
- [x] Publish exact source checkpoint `091e3d7d` and bind tree `45eee43c`.
- [ ] Observe and independently review exact current rulesets, protection,
  workflow, app/principal identity, permissions and owner bypass.
- [ ] Install only a separately reviewed configuration and run hosted
  adversarial race tests on an authorized disposable target.
- [ ] Bind protected host/store qualification and an exact hosted receipt.

## Decision record

GitHub's request-body `sha` is classified as a destination-enforced expected
head. The endpoint exposes no expected-base argument. Base, actor, target ref,
checks and policy are rechecked from the exact observation before construction,
but remain local prerequisites until independently reviewed server rules and a
restricted principal are observed under hosted races. This source slice does
not upgrade those predicates to atomic destination guarantees.

## Current target observation - 2026-09-22

Read-only authenticated observations found no repository rulesets, no effective
rules on `main` or `dev`, no `dev` branch protection and no Actions workflows.
The observed `Julesc013` identity is repository owner/admin, not an admitted
restricted broker principal. The observation half of the first pending item is
complete; independent review and exact principal/app identity remain open.
Hosted effects now fail closed on concrete missing controls rather than an
assumed target configuration.
