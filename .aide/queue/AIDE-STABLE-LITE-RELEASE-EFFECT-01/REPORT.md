# Current AIDE qualification and development report

Date: 2026-10-05, Australia/Sydney. This report describes the current source
qualification, keeps the architecture audit visible, and names unfinished
release and operating outcomes. Source-only result; stable release not certified.

## Actual outcome

The current capability repair and export now pass full source validation through
the existing Windows scoped worker. Job `e188c5d70f14453ab20ddbd84dc09e4b` ran
on source `9badd6f951ca854ae4cc5b13079b26b2c3c3fc43`, tree
`91e1d0aa0511e87d2fda698c76bfe1b0f5cf922d` as
`BLACKGLASS-WIN1\CodexSandboxOffline`. All 18 current capability tests passed,
zero failures/errors/skips, in 13.093 seconds. The 49 release/admission/public
fixture checks are explicitly reused from the verified preceding attempt under
six unchanged source/test/version-policy hashes. They were not run again.

Export and full source validation both exited zero; source validation has no
FAIL or WARN lines. The current pack's 847 payload checksums and current CLI/new
binding-schema bytes match. Export replay changed no tracked pack files.
Complete retained log/output trees, receipt, copied inputs and normalized CLI
frames were verified. Scratch is absent; reservation released; process quiescent;
no IO errors. See [actual source result](evidence/capability-payload-current-source-result.json),
[source qualification](evidence/source-qualification.json),
[CLI proof](evidence/capability-payload-current-cli-proof.json) and
[exact preexecution acceptance](evidence/capability-payload-corrective2-acceptance.json).
Post-result source/effect review remains distinct from preexecution acceptance.

## What changed and why

The C1 source repair preserves the v0 capability ledger and adds optional derived
bindings to finite public evidence. Missing implementation/test evidence remains
unknown; source classification does not certify runtime support. Status reports
CURRENT/STALE/UNKNOWN. Validation inspects retained evidence; only explicit ledger
generation refreshes it. Reader budgets/exclusions are source-reader controls,
not OS permission boundaries. Its implementation and earlier red/green proof are
in the [C1 report](../AIDE-CAPABILITY-EVIDENCE-VALIDITY-01/REPORT.md).

Full qualification exposed a controller-authored brief missing 13 required
sections and a legacy unbound ledger. Both were repaired through existing
commands: packet generation, then exact reviewed scan/ledger/overclaim/validate
within nine declared report destinations. The current root binding is complete,
not truncated, over 41 public inputs. These are input identities, not 41
executed capabilities. The four report commands used the unrestricted outer
shell; that route has no containment claim.

The original job `ca2a1e14` stays recorded as FAIL with its 49 passed checks,
14 validation findings and complete retired evidence. The subsequent `af6d35cf`
effect was refused at aggregate admission before worker launch. Its refusal was
preserved, and no automatic retry occurred. The successful job used a separately
reviewed revised envelope; nothing relabels either predecessor as a full PASS.

The real CLI fixture copied 52 public inputs, 2,616,176 logical bytes, then ran
ten commands. Its deliberately stale validation returned failure and preserved
the old binding/ledger; explicit refresh returned CURRENT. That expected
negative result is separate from zero-failure full source validation. Authored
fixture bytes were preserved. Binary test-process hashes and combined raw trees
are distinct from per-CLI LF-normalized decoded-text hashes. Canonical JSON proof
copies use LF; parsed values match the original retained raw CRLF proofs.

## Effective scope, storage and retirement

| Property | Observed result / boundary |
| --- | --- |
| Worker writes | Allocated TMP/cache/output and existing export destination; source and pinned supervisor read-only |
| Supervisor | Existing immutable old ZIP, 24 unchanged pinned dependencies; export disjoint from runtime |
| Temporary envelope | 4MiB scratch + 6MiB logs + 64KiB result; 16MiB export reservation; 900s/2GiB memory/32 processes |
| Shared aggregate | Unchanged 256MiB cooperative admission and monitored growth; not hard/global quota |
| Admission accounting | Existing scratch/retained/control/canonical contents plus scratch+result+2*logs+2MiB metadata+canonical reservation |
| Sampled workspace peak | 4,989,256 bytes; includes logs, sampled every30s; can miss transient allocation |
| Observed process memory peak | 285,949,952 bytes |
| Retained new evidence | 5,000,654 logical bytes; complete logs preserved |
| Existing known execution pools after collection | 232,749,787 logical bytes; scratch0/control13,694,135/retained219,055,652 |
| Retirement | Complete; no active scratch, quiescent process, reservation released |
| Original configuration/assets | Original rawa241 configuration and four stable candidate hashes unchanged |

The sampled workspace peak is compared with scratch plus log allowance; it is
not proof that TMP ever reached a particular maximum or that a hard4MiB quota
exists. Logical bytes above are not allocated disk recovery or whole-machine
measurements. No unknown or unique drive-root/AppData/temp/clone content was
removed. The reported wider500GB remains unmeasured here. Metadata-first checks
of the known pool found no exact large same-size duplicate candidates eligible
for automatic deletion; that says nothing about other directories/machines.

The outer shell/editor/plugin routes remain unrestricted; read isolation remains
unqualified. Source edits and report generation were performed in that outer
session. Only selected worker execution is qualified. This is not the required
ordinary edit/build/Git workflow under a contained outer client. Observer-started
model requests were0; total host/controller/reviewer usage and matched accepted-
outcome efficiency are not established by that counter.

## Repository, specification and release consistency

The [architecture report](../AIDE-ARCHITECTURE-RECONCILIATION-01/REPORT.md) records
reconciliation across 19 existing topic owners and preserves the original
requirement/use-case material. Imported proposed amendments stay proposals;
attachments and optional approval text are not owner approvals or live-call
permission. The [staged roadmap](../../../docs/roadmap/staged-expansion-roadmap.md)
keeps candidate IDs, ordering, support tiers T0-T5 and capability levels L0-L4
separate from implementation and lane qualification. No broad parity claim or
replacement specification is introduced by this source result.

Local main/dev and cached origin/main/dev remain `e3f14e85` on this inspection;
the last actual remote source-sync receipt names that subject. A fresh remote
read is required for a new ref effect. The current task branch has newer local
qualification records; source synchronization follows its own exact review.
Corresponding branch pairs retain their separate tips; no flattening/pruning is
needed. Source integration is separate from stable certification.

The old ZIP remains SHA256 `4a45922b1dc09cf5073c0968fd016d008cb7bc924c2905efe526ffe11f95dab0`.
It predates the C1 payload. No new archive, runtime promotion, tag, publication,
downloaded-consumer check or target adoption occurred in this source slice.

| Remaining gate | Required next evidence |
| --- | --- |
| Current payload delivery | Build from verified current847-entry export, qualify exact new assets/consumers and deterministic replay |
| Aggregate retained lifecycle | Review exact phase reservations and owned disposable/reproducible eligibility; no evidence deletion or quota widening to force fit |
| Outer client | Effective settings and actual model-accessible shell/editor/integration routes; useful constrained ordinary workflow |
| Ten historical message decisions | Exact owner dispositions against retained original history base; source sync grants none |
| Live model and efficiency | Actual bounded-call permission, source/model binding and matched accepted-outcome/whole-overhead measurements |
| Stable release | Exact first-stable technical ACCEPT and delegated effect, fresh downloaded hashes and supported journeys |
| Wider disk cleanup | Bounded local ownership discovery and exact disposable dispositions per machine/volume |
| Downstream value | Qualified adapter adoption preserving project-owned state; FacMan product stays paused |

## Useful independent development

These are bounded candidates under the existing staged roadmap, not admissions
for all features or permission to start a new platform.

| Candidate | Useful increment | Completion evidence |
| --- | --- | --- |
| C2 compatibility | Explain exact schema/version/policy compatibility and unsupported transitions conservatively | Supported pairs and refusal cases; no invented host parity |
| C3 checkpoints | Portable restart identity and recoverable state with explicit owner/authority provenance | Interrupt/resume without duplicate work, loss of authored state or hidden widened scope |
| C4 resources | Finite retained/cache/artifact lifecycle across existing receipt ownership and admission | Aggregate no-double-booking; eligible retirement and refusal; preserve unique evidence |
| C8 explainability | Persist effective host capability/scope and exact unchanged setup blocker | Covered/uncovered routes, invalidation after relevant changes, no unchanged model wakeups |
| C12 attribution | Minimum controller/child/review/retry/repair and context measurement | Deduplicated available counters, unknown coverage preserved, matched acceptance and warm/cold conditions |
| Existing conformance/support lanes | Small role/adapter checks against accepted contracts | Exact T/L coverage and real lane outcomes; declarations remain separate from runtime proof |

Proceed through admitted queue work with existing tools and configured roots.
Do not repeat storage selection, runner construction, specification import,
unaffected full suites or old archive generation merely to add another status
record. The immediate release task is exact current payload qualification;
containment and finite retention also remain essential operating outcomes.

## Verification commands and evidence

- Four existing `capability scan`, `ledger`, `overclaim-report`, `validate`
  commands: exit0; exact declared report paths; source projection only.
- Existing packet generator: all13 required sections;1297 estimated tokens,
  not an actual tokenizer measurement.
- Native `job run` using selected temporary config/manifest: AF6 refused before
  launch; new separately accepted9badd effect PASS and retired.
- Inside successful worker: `export-pack`, full `validate`: exit0; current
  capability test file:18 passed/no skips; 49 previous checks explicitly reused.
- Complete receipt/raw-tree/test-process/ten CLI/copy identities and all847 pack
  checksums verified; original configuration/four old assets unchanged.
- `scripts/aide compile --write`, structural Harness validation, whitespace and
  structured commit checks: scope-appropriate metadata verification. Structural
  Harness checks are not runtime or whole-session qualification.

Changed records live in this WorkUnit, the exact capability reports and existing
queue/generated/root indexes. The actual implementation owner is C1; the
release entry reuses unchanged worker/canaries and introduces no new runner.
