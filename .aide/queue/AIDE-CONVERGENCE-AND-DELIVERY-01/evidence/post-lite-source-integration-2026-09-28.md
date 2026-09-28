# Post-Lite source integration candidate

- Frozen base: `dev@76e17a4c2101a9f75fa1116b9256d331bd2cedb8`.
- Resource setup branch: `task/aide-campaign-resource-setup-01@917ebe80b91b9956b0b1d0cb2dc9db2c4ab2f5e4`; accepted source `5152798b`.
- Partial rollback branch: `task/aide-rollback-partial-recovery-01@9cabad8d4b9933c8261d520012aa7486346778c4`; accepted source `72d1438e`.
- Candidate branch: `task/aide-post-lite-source-integration-01` in the existing primary checkout. No new physical worktree, canonical release output or shared ref changed.
- Resource ancestry was merged in `3a7cd709375a8629518346d1ec82817d6348b95b` with no conflicts. Rollback source regions merged automatically. The only conflicts were the append-only `PLANS.md` and `IMPLEMENT.md` tails; the resolution preserves current release acceptance, the resource setup record and the rollback repair record.
- Combined-source tests, independent integration review, dev movement and release inclusion are **pending**. Existing branch reviews and tests retain their own exact bindings.

## Combined qualification interruption

- Exact merge candidate `e3f126df` passed all 35 managed-workspace tests in
  D job `3333e847866e4ec3afb9241fc259fcfa` (31.034 seconds, exit 0,
  peak memory 239,292,416 bytes, peak scratch 33,931 bytes). Scratch retired
  and reservation released. Independent reviewer `/root/stable_effect_review`
  accepted this candidate for source integration, explicitly excluding the
  then-pending rollback matrix; see the separate review record.
- The initial eight-case rollback D job `98989186eb9047e5ab944ce2878c2f2c`
  stopped during the intentional reparse fixture with a linked-member monitor
  refusal. It has **no test verdict**. The owned process was quiescent. Two
  junction entries were identified in its scratch; both resolved to targets
  inside the same exact job scratch. Only those two junction entries were
  removed, then AIDE `recover` retained the failed result, retired scratch and
  released its reservation. No target or release asset was touched.
- The short junction case ran separately as D job
  `40756c90dd6944a48d09ba31e6577daf`: one pass, exit 0, scratch retired
  and reservation released. This preserves the junction refusal test while
  avoiding a long-lived intentional link during the runner's live scan.
- A seven-case job `9f9c0200d0e542548aa18ad0617d6d85` stopped after four
  printed passes when the live monitor reported an unnamed unexpected member.
  It has **no seven-case test verdict**. AIDE retained the failure, observed
  quiescence, retired scratch and released its reservation. The original
  monitor error lacked path and file-type detail. A narrow diagnostic source
  change is being prepared so the exact member can be identified before
  changing the safety rule or replaying the suite.
- The diagnostic delta adds the relative scratch path, mode, link count and
  file attributes to that refusal while leaving its predicate and cleanup
  behavior unchanged. D job `7f103f52547b485d97716cee33ad741d` passed
  the focused transient-hardlink scanner case (exit 0, scratch retired,
  reservation released). Its source is not covered by the earlier `e3f126df`
  integration review; exact delta review is still required.
