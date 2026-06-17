# Track B Follow-Up Prompts

These prompt shells are queue-planning material. They do not create authority
to move files, delete files, rewrite references, create aliases or shims, add
top-level roots, mutate branches, mutate target repos, call providers/models,
use network services, publish releases, or implement Track A protocol features.

## AIDE-STRUCTURE-02-status-doc-sync

Objective: reconcile stale status and documentation wording that the Track B
audit identified, especially README, DOCUMENTATION, PLANS, OKF routing notes,
latest task packet wording, and historical task metadata summaries.

Scope: docs and generated context/status surfaces only where queue evidence
backs the correction.

Required outputs: changed-files evidence, stale-claim table, source refs,
validation summary, and remaining risks.

Stop state: `needs_review`.

Forbidden: product feature implementation, OKF authority changes, queue
acceptance, generated-output source-truth promotion, file moves, deletes, and
reference rewrites.

## AIDE-STRUCTURE-03-shared-platforms-research-specs-fate-map

Objective: create a no-apply fate map for `shared`, `platforms`, `research`,
and `specs` using repo intelligence, root recycling, and refactor-map evidence.

Scope: report-only fate mapping, candidate ownership, overlap findings,
preservation rules, and validation plan.

Required outputs: fate map report, unresolved decision table, migration risk
notes, validation plan, and no-forbidden-ops evidence.

Stop state: `needs_review`.

Forbidden: moving files, deleting files, archiving files, rewriting references,
creating aliases or shims, or treating candidates as approved migrations.

## AIDE-STRUCTURE-04-dot-tool-roots-interop-policy

Objective: define interop/projection authority for `.agents`, `.codex`, and
other tool-specific guidance surfaces so generated adapters and local tool
state cannot become hidden AIDE truth.

Scope: policy and docs only.

Required outputs: dot-tool interop policy, generated/projection boundary,
allowed/manual sections, validation notes, and no-forbidden-ops evidence.

Stop state: `needs_review`.

Forbidden: installing plugins, calling tool APIs, mutating external service
state, provider/model calls, network calls, deleting local state, or promoting
generated guidance to queue/protocol truth.

## AIDE-STRUCTURE-05-tools-tests-examples-root-plan

Objective: decide whether `tools`, `tests`, `examples`, or `archive` should
ever become top-level roots, or whether existing roots should keep owning those
materials.

Scope: design-only root plan, candidate decision matrix, naming rules, and
validation plan.

Required outputs: add-only-root decision report, risks, alternatives, and
implementation prompt only if a root is justified.

Stop state: `needs_review`.

Forbidden: creating roots, moving files, deleting files, archiving files,
rewriting references, or applying any structural migration.
