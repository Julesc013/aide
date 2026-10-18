### Fresh symbol evidence for a reuse decision

**Objective.** Extend the existing P6 quality discovery owner so a developer can
inspect an existing Python helper before adding or changing behavior. Present
fresh source locations and syntax-based references alongside the existing
recorded owner, documentation and likely tests. The useful consumer is the real
portable_cli_text projection: find its definition and exported callers instead
of duplicating an incorrect raw-source comparison. This is one useful intelligence
increment, not complete semantic ProjectGraph or automatic restructuring.

**Existing mechanisms.** quality explain-file already projects recorded relations
with unverified freshness. quality_repeated_helper_name_candidates uses a regular
expression and identifies same-name leads only. Neither gives fresh, scoped
definitions or references. Retain both contracts and their 23 Q37/Q38 assertions.
Add a small pure standard-library parser in .aide/scripts/quality_symbols.py;
keep bounded ordinary-file IO and CLI composition under aide_lite.py. Bind the
helper to the executing distribution using its existing sibling-loader pattern;
do not import a selected project's code. Export it through the existing manifest.

**User contract.** quality inspect-symbol NAME --path FILE (repeatable) [--json]
takes one exact Python identifier and one to eight explicit relative files.
Read each ordinary source at most 4 MiB and all selected source at most 8 MiB;
the existing quality ledger remains at most 16 MiB. Refuse unsafe/private/linked
inputs and invalid bounds. No recursive discovery, new report writes, cache,
model, network, target import or project execution.

For valid UTF-8 Python, inspect AST definitions (qualified lexical scope, kind,
parameters, source line/end line), calls with the selected final identifier and
matching import declarations. Disambiguate nested functions/classes; ignore
comment/string lookalikes. Calls are syntax matches, not proven runtime targets:
alias rebinding, dynamic lookup, decorators and dispatch remain unresolved.
Do not dump source bodies, literal values, defaults, exception snippets or docstrings.
Include exact file hashes and parser/runtime identity. Bound match lists with
explicit omitted counts and both JSON/text output to 64 KiB; refuse oversized
output rather than emitting an incomplete record without explanation.

Report parsed/not-found separately from missing, unsupported, invalid or unindexed
source. No observed match is not proof of semantic absence; unselected files
remain outside coverage. Older/missing/malformed quality reports cannot hide valid
fresh syntax evidence: retain their separate recorded/unknown state and explain
that recorded owner/test relations are advisory and freshness unverified.
Recheck selected bytes and the captured ledger before output; changed inputs
refuse the observation. These are sequential checks, not atomic snapshots.

**Implementation and validation.** Preserve every old quality/repo test. Add
behavioral tests for exact scopes/locations, async/decorated definitions, calls
and imports, fake names in comments/strings, alias uncertainty, malformed/future
syntax, unsupported files, Unicode, bounds/omissions, missing reports, safe paths,
freshness and changed-during-read rejection. Real fresh CLI processes must remain
read-only without bytecode artifacts, including under an installed distribution.
No claim that syntax matches establish equivalent behavior or sufficient tests.

Qualify source under a reviewed native job; refresh only the existing capability
source binding if required, retaining original FAIL and unchanged classifications.
Then use the existing owned-export reset/oracle, qualify delivered code and an
actual safe-installed Git consumer with customization retained and core absent.
Run the real portable_cli_text source/consumer query and demonstrate exact
projection semantics through an independent expected-binding check. Confirm
no source/ledger writes and unchanged eight frozen release assets.
Finally verify preserved results and fixed changelog preview, review closure and
safely synchronize dev/main. Use the existing controller and pin its exact script.

**Scope and limits.** Maximum three native allocations: source, delivered/installed,
final preview. Same shared configuration digest
61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90 and existing roots,
180-second/1-GiB/32-MiB-scratch/8-MiB-retained limits and reserves. Each source,
job and integration effect requires exact independent review and fresh guards.
No automatic retry, hidden cap increase, new spending/provider, machine change,
other-project mutation or host/session takeover. Existing authorizations persist.
No test deletion or weakened oracle; use actual changed subjects and reuse valid
evidence. Stop/reconcile changed refs, inputs or controls and retain failures.

**Sequence and recovery.** Exact admission permits only the named local task
branch and mapped packet commit. Implementation follows on that branch. Prepare
named promotion records from the start, complete them from actual evidence and
pin the reused integration controller before terminal review. Commit useful
checkpoints in compact-v1 format. If interrupted, read retained receipts before
retrying; finished jobs are not repeated. Retire only this task branch after
observed dev/main sync and postchecks. Preserve both successor branches.

**Current baseline.** Previous turn made progress: offline result exchange passed
source97/delivered97/installed recovery and integrated at 118ab7829f300050394dc67a3af943963acfe218. The live
worktree is clean on dev. Existing host endpoint, target ownership, model budget
and publication prerequisites have not changed and are not re-probed.
This packet is preparation; no implementation, job or external effect has run.

**Admission and preparation.** Independent ACCEPT covered map5d0311d2 and
effect810710f2. Managed checkpoint396c300c preceded implementation. The parser,
existing CLI composition and21 behavioral methods are prepared; all23 original
quality/repo methods remain unchanged. Tests have not executed. Source/job review
precedes allocation. Return0 means selected syntax parsed, with recorded context
separately advisory; partial source coverage returns1 and refusal returns2.

**Source observed.** Source44 passed at41006cce with no failures/errors/skips;
all23 original assertions remain. Job537aee25 retired with collection verified,
scratch absent and reservation released. Reviewed capability refresh preserved
classification bytes and restored CURRENT binding. Original validation failures
remain until the next reviewed export reconciles the added helper and provenance.
Prepared delivered44 and installed portable_cli_text consumer remain unrun.

**Failure and precise continuation.** Job2/64640393 at0e342967 completed ownership6,
export/doctor/validation/pack-status, then failed the task-runner delta assertion
before delivered tests. The command catalogue correctly gained inspect-symbol,
but the expected payload set omitted it. Original overall FAIL and all evidence
remain. Product source is unchanged. The exact catalogue preimage and one-line
transformation are now explicit; no generic allowance replaces the assertion.

The remaining third allocation combines the unstarted delivered44/installed
consumer with the required final preview. It verifies and reuses the exact
successful export and source44; it does not repeat export or product source tests.
All original acceptance checks remain, within unchanged caps/reserves and the
original three-job ceiling. This recovery needs its own exact review.

**Technical closure.** Final job3 passed at ab7ae7c25bda0f41f069e7a59fbe439feba94865: all 44 delivered methods,
safe-installed discovery and independent projection oracle, full validation and
fixed four-commit preview. Source44 and job2's completed export were reused by
exact hashes; its overall failure stays retained. All three jobs retired with
verified collections. No further allocation. REPORT.md records exact limits;
terminal integration remains an independently reviewed effect.
