# Post-Q08 Foundation Risk Register

## Must Fix Before Next Horizon

None.

No finding blocks next-horizon planning. The foundation is complete with warning-level cleanup notes.

## Should Fix Early Next Horizon

1. Stale generated manifest source fingerprint
   - Risk: generated-artifact drift stays noisy and could hide future drift if normalized as background noise.
   - Current mitigation: `aide validate`, `aide compile --dry-run`, and `aide self-check` report it.
   - Recommended action: reviewed generated-artifact refresh after catalog/status/docs cleanup.

2. Missing `aide self-check` command catalog metadata
   - Risk: Contract command metadata does not fully list the implemented Harness command surface.
   - Current mitigation: `scripts/aide --help`, Harness docs, and Q08 docs record the command.
   - Recommended action: bounded `.aide/commands/catalog.yaml` update in a QFIX.

3. Q00-Q03/Q05/Q06 raw status nuance
   - Risk: queue helpers point at old review gates despite later acceptance evidence.
   - Current mitigation: self-check and queue-runner output expose review evidence nuance.
   - Recommended action: queue/status reconciliation task that preserves history.

4. Stale self-check proposed-followup wording
   - Risk: live self-check proposes Q08 review even after Q08 has passed.
   - Current mitigation: live self-check next recommended step is correct.
   - Recommended action: narrow self-check text cleanup.

5. Stale root docs
   - Risk: README and ROADMAP still mention Q08 review as next work.
   - Current mitigation: PLANS and review evidence record Q08 as passed with notes.
   - Recommended action: docs normalization in the same cleanup track.

## Acceptable Deferred

1. Stored self-check report snapshot
   - `.aide/runs/self-check/latest.md` reflects the pre-Q08-review state.
   - It is non-canonical report evidence and should not be treated as live state.
   - It can be refreshed by a future reviewed report-only task or left as implementation evidence.

2. Q00-Q03 missing direct modern review packets
   - Later review and audit packets accepted proceeding with notes.
   - A future cleanup can make this status clearer without changing historical evidence.

3. Full YAML schema validation
   - Harness v0 explicitly remains structural.
   - Deeper schema validation belongs in future compatibility/harness work.

## Strategic Future Risk

1. Automation pressure
   - Self-hosting automation may tempt future work to invoke agents automatically.
   - Keep Q08 boundaries intact: report-first, no external workers, no auto-merge, no provider/model/network calls.

2. Generated artifact governance
   - Generated outputs are useful enough that future work may start treating them as truth.
   - Keep `.aide/` and `.aide/queue/` canonical and make generated refreshes reviewed.

3. Bridge overreach
   - Dominium Bridge could become product semantics if future work imports too much XStack or Dominium law.
   - Keep XStack Dominium-local and bridge overlays downstream-specific.

4. Compatibility overbuild
   - Compatibility could grow into a migration platform before the repo needs it.
   - Preserve Q06 posture: versioned, conservative, no-op-safe by default.
