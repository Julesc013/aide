# Qualified local dependency recording

The optional source-runtime CLI can record a request, recipient delivery receipt,
native acceptance, returned result and separate requester adoption. It preserves
one logical request across duplicate delivery and process restarts, refuses
conflicting revisions and unmet obligations, and leaves native task authority
and unrelated work independent.

- [Runtime evidence](evidence/second-result.json): 47 API/actual-CLI/state methods
  passed without skips. The [original failure](evidence/first-result.json) remains.
- [Pack evidence](evidence/pack-result.json): six ownership tests, full validation,
  actual exported-State checks and changelog preview checks passed. All jobs were
  collected, digest-verified and retired. No model calls were made by these jobs.
- The development pack has 858 files / 4,421,128 bytes. Runtime-only tests stay
  outside Lite. Published Lite 1.0.0 archives and metadata remain unchanged.
- Source, effects and the byte-identical test-path mapping have independent
  reviews. Exact final integration uses `evidence/integration-effect.json` and
  the observed local `evidence/integration-result.log`, never assumed ref state.

This is cooperative local recording. It does not establish authenticated peers,
automatic delivery to existing desktop workers, process containment, independent
request cancellation, binding replacement or actual cross-project adoption.
Those remain parent workflow increments. DiskEd adoption still awaits native
writer ownership; no live target was changed. Whole-task model cost is unknown.
