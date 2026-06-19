# Selection Strategy Review

The projection selects a small deterministic source set:

- queue status records for build/resume state
- predecessor acceptance/check reports
- capability/conformance validation reports
- Reconciler validation report
- OKF index
- planning and implementation logs

No raw repository dump, embedding, model expansion, external resolver, or
network retrieval is used.
