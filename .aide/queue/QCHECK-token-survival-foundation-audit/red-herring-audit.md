# Red-Herring Audit

| Item | Judgment | Why | Evidence Needed |
| --- | --- | --- | --- |
| More Gateway work now | defer | Q19 is safe local/report-only, but forwarding would not save tokens without reviewed gates. | reviewed Q09-Q20, provider credential policy, dry-run adapter tests |
| Live provider adapters now | defer | Q20 is metadata-only and capabilities are unproven. | provider probe policy, credentials boundary, route/eval gates |
| Router execution | defer | Q17 route decisions are advisory; execution would bypass review if enabled too early. | hard-floor tests plus execution dry-run |
| Cache hits for code edits | keep forbidden | Could reuse stale/unsafe context. | explicit semantic-cache policy and invalidation proof |
| Larger generated docs | reduce | Docs are useful, but more prose does not directly reduce tokens. | evidence docs are used by review packets |
| Golden tasks only testing AIDE | keep but expand | Good substrate gate, not product quality proof. | real coding-task golden suite |
| Token ledger without exact tokenizer | keep | Useful trend signal, not billing proof. | exact tokenizer/billing later |
| Provider metadata before execution | keep/freeze | Safe contract foundation, but low immediate token savings. | Q21 deterministic tool adapter value |
| Commander/UI/mobile next | defer | Does not serve token survival before core proof. | external repo usefulness and quality evals |
| Autonomous loops | defer hard | Would be unsafe before review/eval gates mature. | policy, eval, rollback, and human gate proof |
