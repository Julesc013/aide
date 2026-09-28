# Extracted Lite job owner: source qualification

Date: 2026-09-29. WorkUnit: `AIDE-LITE-EFFICIENCY-01`.

## Frozen subject and repair

- Source candidate `b117f0f8889eb06374e5936f3f2fd47773c0b673` (tree `e2ebd3485944524e48c03a8e0b6d4f4d3fc5ca57`) exported the existing Windows job owner and direct dependencies. Its independent review by `/root/stable_effect_review` returned `REQUEST_CHANGES`: removing `.aide/queue/index.yaml` from a source checkout would bypass maintainer job admission.
- Superseding source `26f343b7764de3e3eb6396a6fd0c9fe1704c874b` (tree `68e62501cae0ba33f68d6ef2a4a6aaeca28afe3e`) requires an extracted pack identity and valid payload checksums before portable admission. A source checkout with a runner but no queue index refuses. The new regression covers that case.
- The same independent reviewer returned `ACCEPT` for dev source integration of the superseding source. It did not accept the rejected candidate, a real Codex effect, stable release bytes or publication.

## Exact bounded results

Both jobs used `.aide.local/execution.json` and the owner-selected shared D: scratch, retained and control roots. The config reserved at least 10 GiB disk, 4 GiB physical memory and 4 GiB commit headroom, with per-job limits of 1 GiB scratch, 256 MiB retained, 2 GiB memory, 16 MiB logs, 3600 seconds, 32 processes and 100000 entries. `job inspect` reported no active job before each launch.

| Source | Job | Command and result | Receipt SHA-256 | Peak memory / scratch |
| --- | --- | --- | --- | --- |
| `b117f0f8` | `432242b202fb44db9eaa69b7110fde30` | `python -m unittest discover -s .aide/scripts/tests -p test_export_import.py -k test_extracted_export_pack_waits_and_runs_job_without_source_checkout -v`: 1/1 PASS | `04fe3830b2f2f41a2549e307cd0c683a55d2e13f2d2a452228a7b3e1a03ebe40` | 255467520 / 430 bytes |
| `26f343b7` | `ef76094d0fd04fcc833a60fdcb469ccf` | Same command plus `-k test_source_checkout_missing_queue_index_cannot_bypass_job_guard`: 2/2 PASS | `a30160694870ebbfbedecc8edce37b3c6fd9b7abeb42d93a88166a7f5876b951` | 255459328 / 671 bytes |

The second extracted-ZIP consumer configured finite roots in its disposable target, inspected and ran a source-bound Python job using the delivered CLI. The exact target HEAD/tree were recorded in its job manifest, not inferred from AIDE's checkout. Outer jobs exited 0, their scratch paths were absent and their shared reservation was released; retained receipts and bounded logs remain under the shared D: retained root. The reviewer independently checked the second receipt hash and cleanup.

## Boundaries

Safe target import still skips `core/**`; the extracted pack runs the owner against an explicitly configured Git working root. The source guard does not claim resilience to deletion of both source markers, and pack checksums establish payload consistency rather than third-party authenticity. This qualification is Windows-only. It does not establish live Codex dispatch, total model usage, a current canonical release archive, native/hosted operation or stable publication.
