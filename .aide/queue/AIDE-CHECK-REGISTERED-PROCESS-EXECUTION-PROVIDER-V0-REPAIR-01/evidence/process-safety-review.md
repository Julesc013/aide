# Process Safety Review

Independent behavior checks used fake runners, fake probes, and fake decoders.
No live Dominium command was rerun.

Observed safety properties:

- invalid spec: zero launches;
- failed precondition: zero launches;
- capability binding mismatch: zero launches;
- provider binding mismatch: zero launches;
- valid invocation: exactly one launch;
- `shell`: false on receipt and fake runner call;
- launch metadata: current invocation only;
- environment in launch metadata: digest manifest, not raw environment values;
- stream summary: scrubber applied before committed excerpt;
- timeout: represented separately from decoder/domain result and marked
  incomplete;
- state-probe coverage: declared coverage preserved;
- mutation observation: scoped to declared probe coverage.

The provider remains a registered-process provider only. It is not a generic
command CLI or universal execution ontology.
