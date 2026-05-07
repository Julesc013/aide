# QCHECK Cross-Repo Adapter Readiness Audit

Checkpoint identity: `QCHECK-cross-repo-adapter-readiness-audit`

Date: 2026-05-07

## 1. Executive Verdict

Verdict: `PASS_WITH_WARNINGS`

AIDE's local QFIX/Q21/Q24 surfaces are substantially coherent: Q09-Q20 are
reconciled as accepted-with-notes, AIDE Lite has a canonical test command,
`aide-lite-pack-v0` exports with a clean boundary, fixture import evidence
exists, and the Q24 adapter compiler renders concise preview/managed guidance
without provider/model/network calls. The handover warning is significant:
Q22 and Q23 are not present as AIDE queue evidence, and the available local
Eureka/Dominium repos do not show the Q21 pack imported. AIDE is ready for a
controlled Eureka import/handover pilot, but it is not ready to claim that the
Eureka handover has already been proven.

- Current highest reliable phase: Q24 inside AIDE, plus Q21 fixture import.
- Current highest claimed phase in AIDE queue: Q24 `needs_review`.
- Target-pilot proof: missing for Q22/Q23 in this workspace.
- Safe to begin Eureka handover: conditional, import-pilot first.
- Immediate next action: run a bounded Eureka AIDE Lite import/handover pilot in
  the Eureka repo, preserving existing Eureka `.aide/` contract files and
  measuring a real Eureka packet.

## 2. Binding Goal Assessment

Binding goal:

```text
Using AIDE reduces token usage and charges for equivalent-quality work.
```

Current evidence for token reduction is strong inside AIDE:

- Latest AIDE task packet: 3,716 chars / 929 approximate tokens.
- `root_history_baseline`: 259,044 chars / 64,761 approximate tokens.
- Estimated task-packet reduction: 98.6 percent.
- Latest review packet: 6,658 chars / 1,665 approximate tokens.
- `review_baseline`: 28,058 chars / 7,015 approximate tokens.
- Estimated review-packet reduction: 76.3 percent.
- Latest context packet: 1,943 chars / 486 approximate tokens.
- `repo_context_baseline`: 276,866 chars / 69,217 approximate tokens.
- Estimated context-packet reduction: 99.3 percent.

Current quality-preservation evidence is substrate-level:

- AIDE Lite `doctor`, `validate`, `selftest`, and `test` pass.
- Verifier passes.
- Golden tasks pass 6/6.
- Review packet generation passes.
- Gateway and provider commands remain no-call/report-only or metadata-only.
- Adapter validation passes and rejects full-history/full-repo style guidance.

Missing evidence:

- No real Eureka Q22 token-saving report exists in this AIDE repo or the
  available local Eureka repo.
- No real Dominium Q23 doctrine-heavy token-saving report exists in this AIDE
  repo or the available local Dominium repo.
- No target-specific golden tasks exist yet for Eureka or Dominium.
- No evidence proves arbitrary coding quality, only AIDE substrate behavior and
  packet structure.

Verdict against binding goal: partially satisfied. AIDE can honestly claim
compact packet generation and local substrate gates. It cannot yet claim
cross-repo token-cost reduction for Eureka/Dominium or arbitrary coding-quality
preservation until target pilots produce evidence.

## 3. Post-QFIX State

QFIX-01 result:

- Q09-Q20 have review files with `PASS_WITH_NOTES`.
- Q09-Q20 queue index/status files are now `passed`.
- Q18 task/status/index drift was fixed.
- `.aide/profile.yaml` no longer points at Q09-era focus.
- `.aide/commands/catalog.yaml` distinguishes implemented, report-only,
  metadata-only, planned, and deferred command families.

QFIX-02 result:

- Canonical AIDE Lite test command: `py -3 .aide/scripts/aide_lite.py test`.
- Canonical command passes.
- `selftest` remains supported and passes.
- Raw unittest discovery without `-t .` passes.
- The old `py -3 -m unittest discover -s .aide/scripts/tests -t .` command
  still fails and is documented as invalid/non-canonical for the hidden
  `.aide` path.

Remaining foundation inconsistencies:

- `scripts/aide self-check` no longer recommends stale Q09, but after Q24 it
  still proposes QFIX-02/Q21-era followups. This is guidance drift and should be
  cleaned in a small future reconciliation, not hidden.
- QFIX-01, QFIX-02, Q21, and Q24 all correctly stop at `needs_review`.
- Q22/Q23 are absent from the AIDE queue despite earlier prompts existing in
  chat history.

## 4. Export / Import State

Pack path: `.aide/export/aide-lite-pack-v0/`

Present artifacts:

- `manifest.yaml`
- `checksums.json`
- `install.md`
- `import-policy.yaml`
- `README.md`
- `export-report.md`
- portable payload under `files/`

Latest export report:

- included files: 122
- checksums: 126
- boundary result: PASS
- provider/model calls: none
- network calls: none
- raw prompt storage: false
- raw response storage: false

Portable includes:

- AIDE Lite script and tests.
- policies, prompts, verification templates, starter golden tasks.
- context compiler configuration.
- cache/local-state boundary docs.
- Gateway no-call skeleton metadata.
- offline provider metadata/contracts.
- import/export policy and target-neutral memory/profile templates.
- adapter policy, targets, and templates after Q24.

Excluded classes:

- source repo identity
- source repo queue history
- source repo memory
- generated context
- generated reports
- route decisions
- cache-key reports
- gateway status reports
- provider status reports
- eval runs
- outcome ledgers
- local state
- secrets
- raw prompts
- raw responses

Fixture import:

- Q21 fixture dry-run and import passed.
- Fixture target ran doctor/snapshot/index/pack/estimate.
- Fixture target packet was 3,789 chars / 948 approximate tokens.
- Fixture did not receive source AIDE queue, memory, generated context, reports,
  cache, route, gateway, provider status, `.aide.local/`, `.env`, or secrets.

Warning:

- Current pack manifest records `source_dirty_state: true` because the audit
  command sweep refreshed generated artifacts before the pack was regenerated.
  The boundary result remains PASS.

## 5. Eureka Pilot State

Q22 AIDE queue evidence: missing.

Read-only local Eureka inspection:

- Path inspected: `D:\Projects\Eureka\eureka`
- Branch: `main`
- Commit: `4c726f849c39763476fa24b81529c7d0d282c844`
- Worktree: clean.
- `.aide/` exists, but it is an older Eureka contract/profile surface, not the
  Q21 AIDE Lite pack import.
- No `.aide/context/latest-task-packet.md`.
- No `.aide/memory/project-state.md`.
- No Q22 evidence directory.
- `.aide.local/` is not ignored in the inspected Eureka repo.

Conclusion: Q22 was not run in the available Eureka repo. No real Eureka
token-reduction or packet-quality evidence is available from this workspace.

## 6. Dominium Pilot State

Q23 AIDE queue evidence: missing.

Read-only local Dominium inspection:

- Path inspected: `D:\Projects\Dominium\dominium`
- Branch: `main`
- Commit: `5a3f5d84a5e3cdeda52cd4fcc4c682e120dbd9d0`
- Worktree: dirty before inspection with:
  - `M data/audit/validation_report_FAST.json`
  - `M docs/audit/VALIDATION_REPORT_FAST.md`
- `.aide/` is absent.
- No `.aide/context/latest-task-packet.md`.
- No `.aide/memory/project-state.md`.
- `.aide.local/` is ignored.

Conclusion: Q23 was not run in the available Dominium repo. No real
doctrine-heavy token-reduction or doctrine-context evidence is available from
this workspace.

## 7. Adapter Compiler State

Policy and definitions:

- Adapter policy: `.aide/policies/adapters.yaml`
- Targets: `.aide/adapters/targets.yaml`
- Templates exist for Codex/AGENTS, Claude Code, Aider, Cline, Continue,
  Cursor, and Windsurf.
- Optional VS Code target is defined as disabled/preview-only.

Commands:

- `adapter list`: PASS
- `adapter render`: PASS
- `adapter preview`: covered by Q24; not rerun in the compact audit sweep.
- `adapter validate`: PASS
- `adapter drift`: PASS
- `adapt`: Q24 evidence shows deterministic managed-section behavior.

Generated outputs:

- `.aide/generated/adapters/AGENTS.md`
- `.aide/generated/adapters/CLAUDE.md`
- `.aide/generated/adapters/aider.conf.yml`
- `.aide/generated/adapters/clinerules`
- `.aide/generated/adapters/continue-checks/aide-token-survival.md`
- `.aide/generated/adapters/cursor-rules/aide-token-survival.mdc`
- `.aide/generated/adapters/windsurf-rules/aide-token-survival.md`
- `.aide/generated/adapters/manifest.json`
- `.aide/generated/adapters/drift-report.md`

Safety:

- Only `AGENTS.md` is written as a managed section.
- Claude/Aider/Cline/Continue/Cursor/Windsurf outputs are preview-only.
- Generated outputs are marked non-canonical.
- Templates are compact: individual generated guidance files are roughly
  962-1,325 chars, excluding manifest/drift report.
- Guidance points to compact packets, validation, evidence, review gates, and
  local-state boundaries.
- No root `CLAUDE.md`, `.aider.conf.yml`, `.clinerules`, `.continue`,
  `.cursor`, `.windsurf`, or `.vscode` output was written.

Warning:

- At QCHECK start, `.aide/generated/adapters/manifest.json` showed Codex
  managed-section drift. Running `adapter render` during the audit refreshed it
  to `current`. This confirms drift detection/rendering works, but it also
  shows generated adapter metadata can become stale and should not be treated as
  canonical truth.

## 8. Validation Results

| Command | Result | Exit | Notes |
| --- | --- | ---: | --- |
| `git status --short` | WARN | 0 | Clean at checkpoint start per initial run; generated/report artifacts became dirty after audit command sweep. |
| `git branch --show-current` | PASS | 0 | `main`. |
| `git rev-parse HEAD` | PASS | 0 | `e2088aed6dd32674c00b8d4701ce8c8be784fdde`. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 0 | Harness validation passed with known review/generation warnings. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | 0 | No hard failures; followup guidance still points at earlier QFIX/Q21 sequence. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | 0 | Report-first; no stale Q09 recommendation, but next-step guidance has residual drift. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | 0 | Adapter status current, no hard failures. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | 0 | Token ledger near-budget warnings only. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | 0 | Internal AIDE Lite checks pass. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | 0 | Canonical AIDE Lite test command passes. |
| `py -3 .aide/scripts/aide_lite.py snapshot` | PASS | 0 | Wrote no-content repo snapshot, 1,017 files. |
| `py -3 .aide/scripts/aide_lite.py index` | PASS | 0 | Wrote repo map, test map, and context index. |
| `py -3 .aide/scripts/aide_lite.py context` | PASS | 0 | Wrote context packet, 1,943 chars / 486 approximate tokens. |
| `py -3 .aide/scripts/aide_lite.py verify` | PASS | 0 | Checked 89 files, 6 changed files at that time, 0 warnings/errors. |
| `py -3 .aide/scripts/aide_lite.py review-pack` | PASS | 0 | Wrote review packet, 6,658 chars / 1,665 approximate tokens. |
| `py -3 .aide/scripts/aide_lite.py ledger scan` | PASS | 0 | Wrote ledger records and summary; 3 near-budget warnings. |
| `py -3 .aide/scripts/aide_lite.py ledger report` | PASS | 0 | 83 records, 3 near-budget warnings. |
| `py -3 .aide/scripts/aide_lite.py eval list` | PASS | 0 | 6 golden tasks listed. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 0 | 6/6 golden tasks passed. |
| `py -3 .aide/scripts/aide_lite.py eval report` | PASS | 0 | Golden task report available. |
| `py -3 .aide/scripts/aide_lite.py outcome report` | WARN | 0 | Advisory packet-too-large warning; no hard failure. |
| `py -3 .aide/scripts/aide_lite.py optimize suggest` | PASS | 0 | Advisory recommendation only. |
| `py -3 .aide/scripts/aide_lite.py route list` | PASS | 0 | Advisory/no-call. |
| `py -3 .aide/scripts/aide_lite.py route validate` | PASS | 0 | Routing metadata valid. |
| `py -3 .aide/scripts/aide_lite.py route explain` | PASS | 0 | Advisory route decision written; no execution. |
| `py -3 .aide/scripts/aide_lite.py cache status` | PASS | 0 | `.aide.local/` boundary protected. |
| `py -3 .aide/scripts/aide_lite.py cache report` | PASS | 0 | Metadata-only cache keys refreshed. |
| `py -3 .aide/scripts/aide_lite.py gateway status` | PASS | 0 | No-call Gateway status. |
| `py -3 .aide/scripts/aide_lite.py gateway endpoints` | PASS | 0 | Forwarding endpoints forbidden. |
| `py -3 .aide/scripts/aide_lite.py gateway smoke` | PASS | 0 | No-call smoke passed. |
| `py -3 .aide/scripts/aide_lite.py provider list` | PASS | 0 | 13 provider families listed. |
| `py -3 .aide/scripts/aide_lite.py provider status` | PASS | 0 | Credentials false, live calls false. |
| `py -3 .aide/scripts/aide_lite.py provider validate` | PASS | 0 | Offline provider metadata valid. |
| `py -3 .aide/scripts/aide_lite.py provider probe --offline` | PASS | 0 | Explicit no-call offline probe. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 0 | 122 files, 126 checksums, boundary PASS. |
| `py -3 .aide/scripts/aide_lite.py adapter list` | PASS | 0 | Targets listed. |
| `py -3 .aide/scripts/aide_lite.py adapter render` | PASS | 0 | Generated previews/manifest/drift report refreshed. |
| `py -3 .aide/scripts/aide_lite.py adapter validate` | PASS | 0 | Adapter outputs pass token-survival checks. |
| `py -3 .aide/scripts/aide_lite.py adapter drift` | PASS | 0 | Codex current, others preview-only. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 0 | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 0 | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 0 | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 0 | 8 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 0 | 112 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests -t .` | EXPECTED_FAIL | 1 | Old invalid hidden-path discovery shape; documented by QFIX-02. |
| `git check-ignore .aide.local/` | PASS | 0 | `.aide.local/` ignored. |
| `git status --ignored --short .aide.local .aide.local/` | PASS | 0 | No tracked/ignored local state shown. |
| Broad `rg` secret scan | PASS_AFTER_INSPECTION | 0 | Matches were policy/test/path terms; no real secrets found. |
| Strict key-shaped `rg` scan | PASS | 1 | No long provider-key/private-key matches. |

## 9. Security / Privacy / Local-State

- `.aide.local/` is ignored in AIDE and not tracked.
- No `.aide.local/` contents were read or committed.
- No `.env` content was committed.
- No raw prompt logs or raw response logs were found.
- Provider metadata remains offline and credentials are not configured.
- Adapter outputs contain guidance only; no provider keys or credentials.
- Export pack boundary excludes source-specific state and local state.
- Strict secret scan found no key-shaped credentials.

## 10. Token / Quality Matrix

| Surface | Chars | Approx Tokens | Baseline | Reduction | Quality Gate | Limitation |
| --- | ---: | ---: | --- | ---: | --- | --- |
| AIDE task packet | 3,716 | 929 | `root_history_baseline` 64,761 tokens | 98.6% | verifier/golden/review available | AIDE repo only |
| AIDE review packet | 6,658 | 1,665 | `review_baseline` 7,015 tokens | 76.3% | evidence packet structure | depends on evidence quality |
| AIDE context packet | 1,943 | 486 | `repo_context_baseline` 69,217 tokens | 99.3% | context refs/no-content map | not semantic compression proof |
| Q21 fixture task packet | 3,789 | 948 | fixture baseline not material | n/a | doctor/snapshot/index/pack pass | fixture only |
| Eureka task packet | missing | missing | missing | missing | missing | Q22 not run |
| Dominium task packet | missing | missing | missing | missing | missing | Q23 not run |
| Adapter guidance files | 962-1,325 | approx 241-332 | no baseline needed | compact by design | adapter validate/drift | advisory only |

## 11. Readiness Matrix

| Area | Ready | Evidence | Blockers | Next Action |
| --- | --- | --- | --- | --- |
| AIDE Pack | Conditional yes | Q21 export, checksums, fixture import, Q24 pack inclusion | source dirty metadata from audit sweep | Review Q21/Q24, then use pack in target pilot |
| AIDE Lite | Yes for repo-local use | test/selftest/unittest pass | old `-t .` command invalid by design | Keep canonical `aide_lite.py test` |
| Export/import | Yes for fixture/import workflow | Q21 fixture import PASS | no real target import proof | Run Eureka import pilot |
| Eureka pilot | No | local read-only repo lacks Q21 import | existing older `.aide/`; `.aide.local/` not ignored | Run controlled Q22/Eureka import branch |
| Dominium pilot | No | local read-only repo lacks `.aide/` | unrelated dirty files in Dominium | Run Q23 only after Eureka handover or separate branch |
| Adapter compiler | Conditional yes | Q24 commands/tests pass, previews generated | needs target proof | Use in target after local import |
| Gateway skeleton | Not for handover execution | no-call smoke PASS | forwarding forbidden | Defer live Gateway |
| Provider metadata | Not for handover execution | offline validate PASS | no probes/credentials/live calls | Defer live provider work |

## 12. Red-Herring / Overbuild Audit

| Candidate | Decision | Reason |
| --- | --- | --- |
| Gateway skeleton | Defer | Useful boundary record, but premature for Eureka handover execution. |
| Provider metadata | Defer | Correctly no-call; not needed until target packet workflow proves value. |
| Adapter compiler | Keep with evidence | Directly helps existing tools use compact packets, but needs target proof. |
| Route profiles | Keep advisory | Useful for no-call decision records; do not build execution before pilots. |
| Cache keys | Keep metadata-only | Helps future reuse discipline; no response cache yet. |
| Controller recommendations | Keep advisory | Good signal, but warnings should not drive autonomous changes. |
| Generated adapter files | Keep preview-only | Useful handover aids; not canonical truth. |
| Excessive queue ceremony | Simplify in targets | AIDE self-hosting ceremony should not be copied wholesale into Eureka. |

## 13. Handover Recommendation

Readiness: conditional.

Do hand over:

- `.aide/export/aide-lite-pack-v0/`
- install/import docs
- target-neutral memory/profile templates
- adapter templates/previews
- canonical validation command: `py -3 .aide/scripts/aide_lite.py test`

Do not hand over:

- AIDE queue history
- AIDE project memory
- generated AIDE context/reports/cache/route/gateway/provider status
- local state
- secrets
- generated adapter outputs as canonical root truth

Recommended Eureka operator command, on a branch in the Eureka repo:

```text
py -3 D:\Projects\AIDE\aide\.aide\scripts\aide_lite.py import-pack --pack D:\Projects\AIDE\aide\.aide\export\aide-lite-pack-v0 --target D:\Projects\Eureka\eureka --dry-run
```

Then inspect conflicts with the existing Eureka `.aide/` contract. Do not
overwrite it destructively. The first real Eureka handover task should be an
import reconciliation pilot, not a product feature.

## 14. Next Queue

Next 3:

1. `Q22-RUN-eureka-aide-lite-import-handover` - run in `julesc013/eureka`,
   reconcile existing Eureka `.aide/`, ensure `.aide.local/` ignore, generate
   Eureka packet, and measure real token reduction.
2. `Q23-RUN-dominium-aide-lite-import-pilot` - run in `julesc013/dominium`
   after protecting unrelated dirty files; generate doctrine-aware packet and
   doctrine-context report.
3. `Q25-target-pilot-adapter-guidance-review` - use real target pilot evidence
   to trim/refine adapter guidance and decide which preview outputs are safe to
   write in target repos.

Next 10:

1. Eureka AIDE Lite import handover pilot.
2. Eureka token-savings and quality review.
3. Dominium AIDE Lite import pilot.
4. Dominium doctrine-context and quality review.
5. Adapter guidance target review.
6. Target-specific golden task starter set for Eureka.
7. Target-specific golden task starter set for Dominium.
8. Cross-repo pack v0.1 cleanup from pilot evidence.
9. Post-pilot checkpoint audit.
10. Only then reconsider provider/Gateway runtime planning.

Non-goals:

- No Gateway forwarding.
- No provider calls.
- No model calls.
- No IDE extensions.
- No autonomous loops.
- No target product changes during import pilots.

Decision gates:

- Eureka handover gate requires safe dry-run/import, `.aide.local/` ignore,
  target-specific memory, latest task packet, token-savings report, and no
  copied AIDE self-hosting state.
- Dominium gate additionally requires doctrine refs by path and no doctrine dump.
- Adapter write gate requires target-specific drift review and manual-content
  preservation evidence.

## 15. Final Recommendation

Proceed with a controlled Eureka import/handover pilot next. Do not begin
Eureka product work, Dominium import work, provider routing, Gateway forwarding,
or live tool integrations until real target-pilot evidence exists.
