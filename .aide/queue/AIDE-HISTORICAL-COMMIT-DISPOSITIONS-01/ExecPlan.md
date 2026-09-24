# ExecPlan: Historical Commit-Message Dispositions

## Objective

Allow an exact, reviewed historical-format disposition to satisfy range
conformance without claiming that the original commit message passed.

## Scope

- Add a source registry, schema, policy, validator, and range-check reporting.
- Bind records to full commit, tree, parents, canonical message hash, and exact
  failed-check messages.
- Add raw-policy mode and adversarial disposable-Git tests.
- Prepare proposed records and an exact decision packet separately from
  mechanism acceptance.

## Non-Goals

- No history rewrite, force push, wildcard, commit-prefix match, blanket merge
  exemption, fabricated historical validation, main promotion, tag, or release.

## Progress

- [x] Inspect current checker, policy, tests, and blocker identities.
- [x] Confirm no existing executable historical-disposition mechanism.
- [x] Create an isolated task branch from current dev.
- [x] Add failing exact-object and adversarial tests.
- [x] Implement schema, policy, registry validation, and range reporting.
- [x] Prove portable export excludes source decision records.
- [x] Prepare proposed exact records and human decision packet.
- [x] Run affected and canonical validation.
- [x] Publish for independent review.
- [x] Preserve the independent `REQUEST_CHANGES` review with two high, one
  medium, and one low finding.
- [x] Repair replacement-object handling, accountable decision binding,
  whole-registry validation, and exact-range whitespace.
- [x] Regenerate and validate the portable checker, policy, schema, tests,
  documentation, local bundle, and preview draft from clean repair source
  `24a49c06ff84d4dbb83bfe608e9363be281b3869`.
- [x] Obtain fresh exact review of `59b886db`: `ACCEPT_WITH_NOTES` for
  mechanism source, with old generated release artifacts excluded.
- [x] Obtain actual responsible-owner decisions for the three proposed records.
- [ ] Integrate eligible source against current dev without restoring older
  release generator or derived artifact snapshots.

## Owner decision execution (2026-09-25)

The owner explicitly accepted A, B, and C in the current conversation. Record
each exact decision as structured JSON with owner provenance, bind the
registry to immutable evidence digests, and verify effective and raw range
behavior. Keep the source candidate and old generated artifacts distinct.
After technical validation, integrate only eligible source against the current
dev generator. A changed source or failed exact binding requires repair and
focused independent review before integration.

## Test Oracle

Without an accepted exact record, the malformed commit fails exactly as before.
An accepted record applies only when full commit, tree, ordered parents,
canonical message hash, exact failed checks, scope, decision, authority, and
record digest all match. Any mutation refuses closed. Raw-policy mode always
reports the original failure.

## Recovery

The mechanism is read-only. Remove or mark a proposed record rejected to keep
it ineffective. Resume from task evidence and committed fixtures; never rewrite
the referenced history.

## Decisions

- Dispositions apply only to range checks; latest, message-file, and hook
  checks remain strict.
- Accepted records bind decision and evidence paths to exact content hashes.
- Accepted records require a structured exact JSON decision by a reviewer in
  the policy allowlist, with a review date inside the permitted window.
- Git replacement objects are disabled for range traversal, message loading,
  and exact object facts; every registry record validates before any can apply.
- The general policy and schema are portable, but this repository's decision
  registry is source-specific and excluded from export.

## Discoveries

- `bfb86c12` has one current message failure; `486e81cd` has thirteen;
  `1011d008` has one bullet-shape failure in `## Why`.
- All three proposed records are visible in range output and remain ineffective.
- A clean source checkpoint is required before regenerating portable artifacts
  with trustworthy provenance.

## Retrospective

The first independent review correctly returned `REQUEST_CHANGES`. Its exact
record verification passed, but it reproduced replacement-ref message
substitution, unbound arbitrary approval, incomplete whole-registry
validation, and two range whitespace errors. The repair closes those source
findings with adversarial tests. All three real historical records remain
proposed, so the original range failures continue to fail exactly and no
integration gate has been bypassed. Portable artifact refresh and independent
rereview remain required before mechanism integration or any exact decisions.
