# Readable complete validation

## Objective and evidence

At 21625bd6a5cf9610e3b8a5a586fb1290bcdf6fe8, retained successful full validation emitted
60,915 findings (60,914 PASS, one WARN), 4,894,357 bytes and 60,917 lines.
Repeated successful per-field assertions dominate. This obscures actionable
findings and exceeds model output limits. Improve presentation in the existing
command; do not rewrite validators, omit checks, add caching, or infer savings
in whole-work cost. This is a bounded P0/P5 usability increment.

## Scope and contract

Keep validate_repo, every collector and common print_messages unchanged.
Only validate defaults to title/status, total and severity counts, every non-PASS
message in original order, and an explicit full-detail hint. Suppress only exact
PASS messages; unfamiliar severities/text remain visible. No truncation of
warnings/failures or unknown messages. --full returns the previous text exactly.
--json returns one versioned object with result, counts and the complete ordered
messages, including duplicates and Unicode. --full and --json are exclusive.
No output files or new authority. Exit code remains the existing validator's.

Existing automation parsing title/status remains compatible; parsers needing
all individual PASS lines must use --full or --json. Add focused regressions
for genuine failures/warnings, duplicates, empty/unknown messages, multiline
messages, large successful lists, exact full compatibility and parser refusal.
Exercise real separate-process CLI validation against disposable minimal repos
with good and broken input; compare all modes and verify no file mutation.

## Sequence and acceptance

1. Exact admission and guarded local task branch from the observed base.
2. Source implementation plus regressions; preserve unchanged existing Lite and
   review-pack assertions. One managed source job. In the export job after binding refresh, retain a real
   repository full validation and compare concise output against its actual
   non-PASS findings/counts. This is output reduction evidence, not cost or speed savings.
3. Separate capability binding refresh and owned export; qualify same tests
   against actual delivered CLI, verify explicit payload changes, doctor,
   full validate and pack status. No claim of live target adoption.
4. Existing fixed changelog preview and terminal review; fresh safe dev/main
   synchronization and retirement of this local task branch only.

Maximum three separately admitted jobs using unchanged existing config and roots:
180 seconds, 1 GiB memory, 32 MiB scratch, 8 MiB retained, 4 GiB memory reserves.
Preserve full logs within caps (do not retain redundant huge JSON and text).
No model calls, release/archive mutation, extra checkout or target effect.

## Recovery and stopping

Preserve failures and exact input hashes; no automatic retries or weakened checks.
Stop for unmet admission, unsafe notes or changed effect. Do not repeat known
native adoption/desktop-binding probes without changed prerequisites. Existing
Lite1.0.0 qualification remains valid for its exact subjects. Full campaign and
whole-outcome efficiency remain incomplete. Branch/status receipts govern actual
integration rather than a planned outcome.

## Progress

Read-only investigation and intake prepared. Intake conservatively flags release
words in exclusions; this explicit child separates source, jobs and integration
and authorizes no release. No implementation, branch or job performed yet.

Admission ACCEPT; guarded local branch prepared. Source presentation and nine
regressions prepared, with27 existing Lite/review assertions unchanged. No job yet.
