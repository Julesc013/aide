# AIDE current qualification and development report

Current outcome: 2026-10-05, Australia/Sydney. Architecture audit baseline:
`3d186d05`; preceding source-sync baseline: `bf559c0a`. This report supersedes
preparation statements only where actual checks and effects below are complete.

## Actual outcome

The attached architecture review was reconciled into the existing specs and
plans. Two demonstrated release-path defects were then repaired. Current source,
local Lite assets and the original configured worker entry are independently
accepted and integrated into main/dev at `21f8677d`. The atomic origin push and
fresh verification succeeded: **88 corresponding local/remote branch pairs
match, with the other 85 tips preserved**. Different branches retain their own
tips; synchronization does not flatten them.

There is a qualified **local Lite 1.0.0 candidate**, with eight successful
consumer cases, current-byte CLI coverage and reproducible archives. There is
no new stable tag or public release. This controller/editor still has Full
Access. Whole-session containment and matched efficiency remain unqualified.
The final record-only closeout uses a separate exact independent review and
normal three-ref synchronization; its local terminal receipt is retained in
`evidence/final-sync-result.log` without a self-referential commit identity.

## Specifications and documentation

The accepted [architecture report](../AIDE-ARCHITECTURE-RECONCILIATION-01/REPORT.md)
reconciles **19 existing topic owners** and preserves **244 original UR/UC
statements**, import-time custody and draft status. Proposed semantic amendments
remain distinct from adopted contracts, implemented behavior, operation grants,
support claims and release certification. No replacement specification, archive,
worktree or new storage layout was created.

The amendments cover compatibility and migrations; worker/session/request/model
boundaries; resource eligibility and enforcement; portable ownership/checkpoints;
asset and learning lifecycles; authority and outcome-based optimization; narrow
extension contracts and conformance; operator explanations; and incremental
implementation. Existing owners and module seams are retained.

README, Profile and runtime descriptions were corrected where they called
existing declaration/projection/bounded implementations wholly planned. Root
PLANS, IMPLEMENT and DOCUMENTATION indexes, queue/status/focus, the compact task
packet and dated roadmap now reflect completed local qualification. Historical
attempts/reviews remain in canonical evidence and Git history. The imported
architecture attachment disappeared after its initial full read; its raw SHA
remains explicitly unknown. Current amended spec identities are independently
bound in [amendment-manifest.json](../../../specs/control-plane/amendment-manifest.json).
This is affected-document reconciliation, not proof that every old archive or
source line has been audited or that the software is perfect.

## Implemented code and delivered behavior

- Stable-build and stable-validate now reserve only their release destination
  through the existing guard. Read-only export no longer incurs an erroneous
  write reservation. Shared packaging and supervisor/output overlap guards stay.
- Recognized public archive/release-test fixtures under authenticated existing
  job TMP inherit that allocation's permissions. A private temporary directory
  had prevented the separate controller from monitoring and retiring public
  bytes. Unmanaged/unrelated temporary behavior remains private; there is no
  global tempfile override, monitoring bypass or AIDE ACL setter.
- Public fixture cleanup refuses changed identities, redirected entries and
  shared files. Readonly-file retirement is confined to verified fixture custody.
- The generated export pack now preserves exact bytes through Git checkout.
  Four CRLF-to-LF checksum mismatches were repaired by a subtree-only -text
  rule and exact restoration from the qualified ZIP; archive/checksum identity
  is unchanged. Root source/Git LF forms are equivalent after normalization.
- The bounded job-inspection projection explains worker placement, run-only
  aggregate admission and uncovered outer routes. It grants no execution rights.
- The original configured runtime was promoted only by replacing its archive
  SHA and adding the 24th pinned dependency. The other 23 hashes, source/output
  paths, limits, account/model route and canonical scope are identical. A real
  native probe through that original entry passed and retired.

A separate pinned export supervisor builds disjoint release outputs. The worker
never rewrites its own supervising runtime. Required source proof is reused
only while its exact inputs match; consumer/replay proof exercised new bytes.

## Verification and resource evidence

| Check | Actual outcome |
|---|---|
| Changed source | 5 admission + 8 public-fixture + 36 release checks: **49 passed**, zero failures/errors/skips |
| Export/repository | Export generation and full validation passed; **846 export checksums** recomputed |
| Existing core/host | **71 previously qualified checks reused** because their source remained unchanged |
| Current delivered consumers | **8 cases passed exactly once**, retaining existing acceptance assertions |
| Public CLI | **38 forms, 39 raw command outputs and 12 raw job-form observations**, all bound to current assets |
| Task OS | Default report behavior and explicit report effects passed, without new lifecycle authority |
| Deterministic replay | All **four assets reproduced byte for byte** |
| Original configured entry | Native `CodexSandboxOffline` pin/config/inspection probe passed |
| Retirement | Current owned jobs/fixtures retired; active/scratch absent, reservations released, collected digests verified |
| Git integration | Independent exact acceptance, fresh guards, normal fast-forwards and atomic three-ref push passed |

The eight cases cover import/update/partial recovery; lifecycle; offline context;
partial CLI; public CLI; forced restart; job forms; and delivered Task OS. Expected
negative command results are retained as negative cases, without skipped checks.

| Job | Peak scratch | Retained bytes |
|---|---:|---:|
| Source `b92f98a4` | 6,095,005 | 4,903,513, including full logs |
| Build `2069e86b` | 8,508 | 13,787 |
| First consumer `dc069cd9` | 29,375,912 | 3,042,992 |
| Remaining consumers `eff8ab1f` | 28,532,513 | 5,809,600 |
| Replay `2e0b0e5e` | 8,294 | Exact retained record in replay-result.json |
| Original entry `7b2c4eba` | 9,988 | 14,780 |

Source peak memory was 307,408,896 bytes; first consumer 330,551,296; remaining
consumers 334,970,880; original entry 218,066,944. Scratch peaks are observations,
not simultaneous sums or hard quotas. Retained values include receipts/logs;
result and log allowances are separate. Parent/reviewer/retry/billing coverage
is incomplete. Deterministic workers made no nested model requests; this does
not establish zero campaign cost or measured savings.

Full source logs made the old single consumer reservation exceed the existing
256 MiB aggregate. Two predeclared serial groups fit fresh locked admission:
40/4/1 MiB scratch/result/log for the first and 34/7/1 MiB for the rest. The cap,
drives, complete evidence and all acceptance assertions were preserved. No
case was dropped or duplicated. Code owned waiting, monitoring and retirement.
Whole-host unchanged-waiting behavior and matched efficiency remain unproven.

[Current proof](evidence/current-qualification.json),
[form coverage](evidence/current-public-form-coverage.json),
[local acceptance](evidence/qualification-acceptance.json),
[original probe](evidence/original-entry-probe-result.json) and
[integration result](evidence/integration-result.json) retain exact source,
asset, receipt and raw-output identities. Required raw evidence remains in the
configured D retained pool, rather than another archive or conversational dump.

## Candidate identity and scope

ZIP SHA256: `4a45922b1dc09cf5073c0968fd016d008cb7bc924c2905efe526ffe11f95dab0`.
TAR SHA256: `4b3e22ee351aa31e9fdb5f50e89affd38ef3908163083058f2b151c0c57d8541`.
Delivered CLI: `f58f1cf419c09938c43d4a34779e9aba0be8d01455163b7e801dfa7d888a0e88`.
Payload source: `a8e004e7235902cd1d290d82cbaccb9a1bd65bb1`; exact tree/pack checksum
identities are in the current proof. Local intended version 1.0.0 and candidate
T3/companion posture are not public stable certification. The old candidate has
exact baseline Git custody without another physical backup.

Approved pools remain `D:/Projects/AIDE/.aide.local/execution/{scratch,retained,control}`.
One heavyweight job at a time; finite phase allowances; 2 GiB memory, 32 processes,
900 seconds per job, 10 GiB disk and 4 GiB memory headroom. The exercised worker
write and Windows process/memory/log boundaries are qualified only within their
recorded routes. Aggregate storage is cooperative admission and monitored growth,
not a hard filesystem quota or global budget. Host management metadata/caches,
other sessions and unrestricted editing/plugin routes remain outside that claim.

Original probe environment: Windows 10.0.19045, Python 3.14.7,
`BLACKGLASS-WIN1\CodexSandboxOffline`, pinned Codex 0.145.0. Actual outer application,
model editing/API/plugin route coverage and read exclusion still require client
setup and a constrained ordinary workflow. Command-only proof cannot close them.

## What can be developed next

The [staged roadmap](../../../docs/roadmap/staged-expansion-roadmap.md) ranks 12
candidate increments. They are useful independent work; each needs its own
bounded WorkUnit, exact scope, acceptance and review before implementation.

| Order | Candidate | Useful next outcome |
|---|---|---|
| First | C1 Truth projections | Source/config/route changes invalidate affected claims; declarations cannot masquerade as runtime proof |
| First | C8 Explainable operations | One actionable failure/resume condition and effective configuration provenance, without unchanged resubmission |
| Next | C2 Compatibility | Old/new reader-writer fixtures, unfamiliar-field preservation and explicit semantic loss/refusal |
| Next | C3 Portable checkpoints | Resume the same work from verified facts/effects/obligations without a replacement checkout |
| Next | C4 Resource ownership | Metadata-first receipts/reachability, hardlink-aware logical versus recoverable allocation and explicit retirement |
| Later | C9 Contributor conformance | One pinned role reference with storage/error/cancellation fixtures and packaging guidance |
| Later | C11 Recipe invalidation | Targeted invalidation for requested/resolved/observed driver/model/template dependencies |
| Consumer-dependent | C5 Request lifecycle | Cancellation of one request preserves others using a shared instance |
| Consumer-dependent | C6 Asset metadata | Discovery/acquisition/qualification/activation and lineage, without automatic downloads or training |
| Consumer-dependent | C7 Lesson correction | Scoped correction/retirement and dependent retrieval invalidation |
| Consumer-dependent | C10 CLI characterization | One use case characterized before extraction; output/exit/effect compatibility preserved |
| Consumer-dependent | C12 Usage attribution | Deduplicate shared/cumulative/parent-child counters; preserve failures, unknowns and verification reserve |

The first bounded C8 inspection projection is delivered; it does not complete
all of C8 or qualify the outer host. Next priority is C1/C8, then C2/C3/C4, which
improve trustworthy status, restart continuity and resource conservation. Fleet,
enterprise, learning, shared inference and additional IDE/native/legacy lanes
remain visible as later separately qualified profiles. Exact support belongs in
T0–T5 posture and L0–L4 capability records; no host parity or untested version
claim was added. FacMan product development remains paused.

## Preserved failures and recovery

Build `27de35f9` refused erroneous export reservation before asset effects.
Repair `46e91fbf` passed five tests/export then failed private-temp validation.
Same-job custody recovery retired its exact public fixture, preserved all
original/helper logs and the failure, and released the reservation. Wrong-SID
observations and bounded setup failures remain recorded. Build `33662de9`
refused because this controller prematurely added an untracked review record;
it retired with all assets unchanged. Keeping that review in an ignored log
reconciled the setup before successful build `2069e86b`. Failed attempts are
not erased, replayed while uncertain or relabelled as successful.

Postintegration pack-status exposed the four generated line-ending mismatches.
The bounded repair and exact working/staged checksum proof are preserved in
[export-byte-preservation.json](evidence/export-byte-preservation.json). No new
archive, replacement suite, source semantics or supervisory permission follows.

## Separate remaining gates

- **Outer client:** effective model editing/tool paths and read/write exclusion,
  followed by one ordinary constrained edit/check/collect/retire workflow.
- **Historical policy:** ten exact message dispositions remain unaccepted;
  permission to synchronize source did not accept them.
- **Live model:** the prepared GPT-6.1 Sol qualification still lacks its local
  invocation permission. Uploaded proposed approval text is not a grant.
- **Efficiency:** live binding, matched accepted-outcome cost/quality and
  whole-host unchanged-waiting evidence remain unfinished; unknown usage stays
  unknown. No repeated refused invocation was attempted.
- **Stable delivery:** exact release-effect acceptance, tag/publication,
  downloaded-byte consumer checks and authorized project tooling adoption.
- **Wider storage:** the reported roughly 500 GB drive/AppData/temp/clone sprawl
  is not measured or reclaimed by these jobs. Unique/unknown work is preserved.
  Verified owned scratch retirement is a narrower result.

The campaign Goal remains active; unchanged blocked effects remain dormant.
Current qualification closes the stale-asset and original-worker selection
boundaries. It does not establish perfect software, whole-session containment,
measured savings or a published stable AIDE release.


## Bounded storage follow-up (2026-10-05)

The existing SESSION WorkUnit completed a read-only check of one recorded
Universal linked worktree. Three tracked source modifications require
preservation. Its owned native regression qualified the fresh-stat file
identity correction; both jobs collected/verified results and retired scratch.
Actual target link/unique-byte and reclaimed-space claims remain unknown/zero.
See [storage report](../AIDE-SESSION-CONTAINMENT-01/STORAGE-REPORT.md).

This source/evidence synchronization is separately reviewed; the four Lite
assets, original configuration and24 supervised dependencies remain unchanged.
Its final actual-ref receipt is retained at
../AIDE-SESSION-CONTAINMENT-01/evidence/storage-final-sync.log. That receipt
determines the observed synchronized head; no self-referential commit identity
is fabricated in this report. Stable tag/publication and remaining external
gates above remain unfinished. No FacMan product work or target cleanup occurs.
