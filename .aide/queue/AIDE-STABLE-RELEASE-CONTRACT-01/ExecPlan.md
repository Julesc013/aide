# ExecPlan: AIDE-STABLE-RELEASE-CONTRACT-01

## Purpose

Define the first stable Lite version, public compatibility and support
contract, and a campaign-scoped publication route without treating a local
preview bundle as a public release.

## Scope and allowed paths

The exact allowlist is in `task.yaml`. Contract owners are the existing
release-versioning and publication-boundary policies, the adopted product
scope/profile document, the root release policy, and their reference docs.
At admission, only this task's queue records, index, four task-relevant intake
outputs, and root plan/execution indexes were edited. Q47/Q48 generators,
local release artifacts, implementation source, hosted settings, target
repositories, and new specification overlays are outside this WorkUnit.

## Dependencies and current facts to verify

- Clean task worktree base: `dev@d4b67c96ff81eb10aeecd6763b538331844619c9`.
- The active release-versioning policy says stable SemVer and a public
  compatibility contract are not established; Q47/Q48 outputs are previews.
- The parent programme's 2026-09-25 owner delegation permits qualified
  release actions but retains independent technical and exact-effect gates.
- The parent controller supplied a read-only 2026-09-25 09:40 UTC GitHub
  observation under `BLACKGLASS-WIN1\Jules`: releases and tags API returned
  no entries, exits 0. This task did not independently make that API call;
  capture its source-bound receipt before deciding version history.
- The existing mandatory-profile matrix is a prior checkpoint, not final
  qualification of this source or eventual assets.
- External analysis note SHA-256:
  `aaf8ab963440f7df049892ccef0eaa10a9fae47850ec68478393f04726f0db7f`.

## Current contract-source plan (2026-09-25)

Objective: define a conditional stable Lite SemVer and public compatibility
rule, a Windows-only local companion profile with no current shipping claim,
and an exact campaign-only path through review gates to a future release
effect WorkUnit. Keep `aide-lite-pack-v0` as the separate portable pack format.

Scope: edit only the allowed versioning/publication/review policies, the
existing adopted scope/profile and release governance documents, their two
release references, root indexes, and this task's evidence/state. Preserve
Q47/Q48 generated files and their no-publish policy/history. No new spec file,
implementation code, target, branch, tag, or network effect.

Dependencies: the owner's recorded 2026-09-25 delegation, the parent
controller's no-entry read-only GitHub history observation, existing support
tier and host-capability definitions, and mandatory-profile coverage gaps.
Do not infer final version, tag, source, asset, or readiness from those inputs.

Verification: structural policy/document consistency, focused existing
release and queue checks where read-only, exact path and whitespace audit,
and independent review of the frozen diff. Expected blocker: this source
change may make generated pack/release previews stale until a later reviewed
integration phase regenerates them; record that state without generating here.

## Non-goals

- No version choice or stable-readiness claim at admission.
- No main merge, tag, upload, publication, protected-ref bypass, retag, or
  changed bytes under an existing release identity in this WorkUnit.
- No global weakening of hard review gates or reinterpretation of Q47/Q48
  preview reports as published evidence.
- No model, provider, target-repo, native, or hosted effect.

## Milestones and progress

- [x] Inspect clean base, governing sources, parent programme and external
  read-only analysis note; compile release intent.
- [x] Prepare this bounded admission packet and record compiler refusal of
  raw release execution.
- [x] Root controller reviewed the exact admission scope and recorded the
  owner's campaign delegation as authority for this routine child; see
  `evidence/controller-admission.md`. Independent technical review remains
  required for the actual version/profile/policy candidate.
- [x] Define a conditional version and public compatibility candidate. The
  parent-supplied hosted observation is admission context; a fresh complete
  local/hosted history receipt is still required at release freeze.
- [x] Define the first stable Lite profile target with candidate CLI forms,
  Windows-only lifecycle apply, support-tier target and excluded profiles.
  Qualification against final assets and predecessor versions remains open.
- [x] Draft campaign-scoped queue/review/publication policy and documentation
  changes, preserving Q47/Q48 history and independent technical gates.
- [x] Run contract/schema/link/regression validation and obtain independent
  exact candidate technical review before any dev integration.
- [x] Retain the `aa3bcfec` REQUEST_CHANGES report and merge current accepted
  `dev` source at `060de472` with both planning histories intact.
- [x] Repair the missing predecessor/conflict CLI forms and record the exact
  committed pack/validate/doctor failures; seek focused superseding review.
- [x] Route generated export/release output to a separate bounded projection
  WorkUnit and establish passing committed combined-candidate machine gates.
- [ ] Route a later exact release-effect WorkUnit after mandatory behavior,
  final artifacts, and support claims qualify.

## Validation and evidence

Admission: `intent compile`, inspect its four outputs, `task inspect`,
`git diff --check`, JSON parse, status and path audit. Record exact commands
and results in task evidence. Contract execution: policy/schema and documentation
validation, affected tests, review of release-history receipt and support
matrix, canonical validate/doctor, and exact diff review. A release-effect
WorkUnit later owns final integrated tests, source/asset freeze, consumer
qualification, independent release verdict, remote effects, and downloaded
byte checks. None of those future checks is claimed as run here.

## Discoveries and decisions

The intent compiler marked the broad release prompt blocked and
`requires_split: true`; its output is intake evidence, not executable
approval. This WorkUnit addresses only the contract slice. The owner
delegation is already recorded; no repeated routine owner response is
proposed, but independent technical review remains required.

## Idempotence and recovery

Re-read queue state, worktree status, source commit, and the external note
digest before resuming. If another worker changes policy or release history,
rebase the contract analysis on observed bytes and request focused review of
the changed scope. Keep draft choices and failed reviews as evidence. Do not
retry an uncertain main/tag/publication effect here; this task has no such
effect authority. A later effect WorkUnit must observe remote state before
replay and must not retag changed bytes.

## Retrospective

The repaired contract source received independent exact `ACCEPT` at
`d38e5839`. Separate projection WorkUnit
`AIDE-STABLE-CONTRACT-PROJECTION-01` regenerated and reviewed local preview
assets, passed committed machine/replay checks and integrated `dev@2defcad5`.
The earlier admission and `aa3bcfec` REQUEST_CHANGES records remain
historical evidence. This WorkUnit selected no version or tag and qualified
no shipping profile or publication effect.
