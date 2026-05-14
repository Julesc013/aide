# Validation

## Baseline

- `git status --short`: PASS, clean.
- `git branch --show-current`: PASS, `main`.
- `git rev-parse HEAD`: PASS, `bf27445fd62e79d39fc2d34c30127f9f360cc8b5`.
- `git rev-list --left-right --count origin/main...HEAD`: PASS, `0 6`; local `main` was six commits ahead of `origin/main` before Q42.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `git diff --check`: PASS.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; pre-existing generated manifest source fingerprint stale warning.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same generated manifest stale warning.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; same generated manifest stale warning and Q41 status metadata drift found before repair.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py intent validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py repo validate`: WARN; existing unknown file classification warnings.
- `py -3 .aide/scripts/aide_lite.py quality validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py refactor validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py roots validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py tools validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py github validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.

## Final

- `git diff --check`: PASS.
- `git branch --show-current`: PASS, `main`.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; pre-existing stale `.aide/generated/manifest.yaml` source fingerprint warning.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same stale generated-manifest warning.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q42 is `needs_review`, Q36-Q42 remain review-gated, and the stale generated-manifest warning remains.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 85 tasks, 85 pass, 0 warn, 0 fail.
- `py -3 .aide/scripts/aide_lite.py repo validate`: WARN; existing unknown file classifications: 146.
- `py -3 .aide/scripts/aide_lite.py quality validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py refactor validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py roots validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py tools validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py refactor map`: PASS; generated current map bundle with no apply behavior.
- `py -3 .aide/scripts/aide_lite.py refactor move-map`: PASS; 0 entries, no file moves.
- `py -3 .aide/scripts/aide_lite.py refactor salvage-map`: PASS; 20 candidate entries, `drop_candidate_is_delete_approval: false`.
- `py -3 .aide/scripts/aide_lite.py refactor aliases`: PASS; 0 aliases, no active aliases or shims.
- `py -3 .aide/scripts/aide_lite.py refactor rewrite-plan`: PASS; 40 candidate entries, no files rewritten.
- `py -3 .aide/scripts/aide_lite.py refactor validate-map`: PASS; all current maps are candidate/no-apply and contain no active move/delete/rewrite/alias/shim flags.
- `py -3 .aide/scripts/aide_lite.py refactor map-status`: PASS; move entries 0, salvage entries 20, aliases 0, rewrite entries 40, `no_apply: true`.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_q42*.py"`: PASS, 10 tests.
- `py -3 .aide/scripts/aide_lite.py intent validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py github validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS; 426 included files, 429 checksums, boundary result PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, boundary PASS, provenance `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q43 Install Plan Model v0"`: PASS; latest task packet unchanged at 1,023 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS; 1,023 approximate tokens, within budget.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id Q42-move-map-salvage-map-path-alias-v0`: PASS; status `needs_review`, classification `complete`, missing evidence 0.
- `py -3 .aide/scripts/aide_lite.py task status --task-id Q42-move-map-salvage-map-path-alias-v0`: NOT_SUPPORTED; `task status` does not accept `--task-id`.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS; Q42 status `needs_review`.
- `py -3 .aide/scripts/aide_lite.py commit check --range bf27445fd62e79d39fc2d34c30127f9f360cc8b5..HEAD --max-count 6`: PASS after local Q42 commit-message repair.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: TIMEOUT twice, once at 184 seconds and once at 604 seconds. Q42 did not modify `core/gateway/**`; this is recorded as residual validation risk.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.
- Targeted `rg` secret scan over requested paths: PASS_AFTER_INSPECTION. Matches were policy, docs, path, generated-reference, regex, and fake-test terms such as `api_key`, `SECRET`, `TOKEN`, `PASSWORD`, `sk-ant`, and `latest-task-packet`; no actual provider key, `.env` content, `.aide.local` state, private key, raw prompt log, or raw response log was found. The requested `tools` path is absent in this repo, so `rg` returned a missing-path diagnostic.

## Boundary Results

- Provider/model calls: none.
- Network calls: none.
- File moves: false.
- File deletes: false.
- Reference rewrites: false.
- Active aliases or shims: false.
- Target repo mutation: false.
