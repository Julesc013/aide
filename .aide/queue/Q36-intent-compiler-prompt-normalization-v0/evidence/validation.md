# Q36 Validation

Validation used `py -3` on Windows PowerShell from `c:\Inbox\Git Repos\aide`.
Commands were local and deterministic. No provider/model/network calls were
introduced.

## Baseline Before Editing

- `git status --short`: PASS, clean.
- `git branch --show-current`: PASS, `main`.
- `git branch --all`: PASS, local `main` and remote `origin/main` observed.
- `git remote -v`: PASS, `origin` observed.
- `git rev-parse HEAD`: PASS, starting HEAD `e170a95554e19c36c4382c3a3b2152747819eb2a`.
- `git tag --list`: PASS, no tags.
- `git check-ignore .aide.local/`: PASS.
- `git diff --check`: PASS.
- `py -3 scripts/aide validate`: PASS before edits.
- `py -3 scripts/aide doctor`: PASS before edits.
- `py -3 scripts/aide self-check`: PASS before edits; Q36 was the next AIDE-local phase.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS before edits.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS before edits.
- `py -3 .aide/scripts/aide_lite.py test`: PASS before edits.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS before edits.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS before edits.
- Q35 status inspection: PASS; Q35 was `passed`.

## Final Structural And Harness Validation

- `git diff --check`: PASS; CRLF normalization warnings only.
- `git branch --show-current`: PASS, `main`.
- `git check-ignore .aide.local/`: PASS.
- `py -3 scripts/aide validate`: WARN, 148 info / 1 warning / 0 errors. Warning: generated manifest source fingerprint is stale after Q36 source-truth changes. Q36 did not refresh `.aide/generated/manifest.yaml` because that path is outside this phase.
- `py -3 scripts/aide doctor`: WARN with the same generated-manifest warning.
- `py -3 scripts/aide self-check`: WARN with the same generated-manifest warning and Q36 still in progress at command time.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS after moving intent guidance out of the generated AGENTS managed section.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.

## Intent Command Validation

- `py -3 .aide/scripts/aide_lite.py intent compile --prompt "next"`: PASS; `task_class=context`, `risk_class=low`, `sizing_class=audit_only`.
- `py -3 .aide/scripts/aide_lite.py intent compile --prompt "fix everything"`: PASS; `task_class=repair`, `risk_class=high`, `sizing_class=split_required`.
- `py -3 .aide/scripts/aide_lite.py intent compile --prompt "delete old XStack stuff"`: PASS; `task_class=refactor`, `risk_class=destructive`, `sizing_class=blocked`.
- `py -3 .aide/scripts/aide_lite.py intent compile --prompt "merge dev to main"`: PASS; `task_class=git`, `risk_class=release`, `sizing_class=blocked`.
- `py -3 .aide/scripts/aide_lite.py intent compile --prompt "install AIDE into Dominium"`: PASS; `task_class=install`, `risk_class=external_side_effect`, `sizing_class=two_shot`.
- `py -3 .aide/scripts/aide_lite.py intent compile --prompt "Plan Q37 Repo Intelligence Index v0 from the current AIDE repository state"`: PASS; latest packet restored to Q37 sample with `task_class=audit`, `risk_class=low`, `sizing_class=audit_only`.
- `py -3 .aide/scripts/aide_lite.py intent validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py intent examples`: PASS, 10 examples, no writes.
- `py -3 .aide/scripts/aide_lite.py intent status`: PASS, latest packet is the Q37 sample.

## Tests And Golden Tasks

- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q36_intent_compiler.py`: PASS, 14 tests.
- Direct `py -3 -m unittest .aide/scripts/tests/test_q36_intent_compiler.py`: FAIL because hidden `.aide` is not an importable top-level package path. This is the known non-canonical form from QFIX-02; supported discovery passed.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 41/41 golden tasks. Generated eval run reports were restored because `.aide/evals/runs/**` is outside Q36 scope.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 203 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.

## Recovery, Git, GitHub, Changelog, Ledger, And Review Commands

- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS after amending the docs commit message to Q27 structured trailers.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS, preview-only; generated changelog outputs restored as out-of-scope.
- `py -3 .aide/scripts/aide_lite.py changelog validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect`: WARN when run after generating the Q37 task packet because Q37 has no queue item yet; rerun with `--task-id Q36-intent-compiler-prompt-normalization-v0` passed. After Q36 status was updated, explicit inspect showed `status=needs_review`, `classification=complete`, `missing_evidence=0`, and `noop_already_complete`.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS.
- `py -3 .aide/scripts/aide_lite.py task noop-check --task-id Q36-intent-compiler-prompt-normalization-v0`: PASS; `continue_from_status_and_evidence`.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS, non-mutating.
- `py -3 .aide/scripts/aide_lite.py github validate`: PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, no raw prompt/response storage; token ledger outputs restored as out-of-scope.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify`: WARN, 0 errors. Warnings came from generated previews pending restore and from the verifier using the latest Q37 task packet while Q36 files were still dirty.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, wrote `.aide/context/latest-review-packet.md`, 2353 estimated tokens, within budget.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q37 Repo Intelligence Index v0"`: PASS, wrote `.aide/context/latest-task-packet.md`, 918 estimated tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 918 estimated tokens, within budget.

## Export Pack

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS; 245 included files, 248 checksums, boundary PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, boundary PASS, provenance `DIRTY_SOURCE_RECORDED`.

## Secret Scan

Targeted secret scan was run with ripgrep after evidence updates. Matches were
policy/example/reference strings, including forbidden-token patterns and safe
local-state documentation. No actual provider credential, API key, private key,
or `.aide.local/` content was found or committed.
