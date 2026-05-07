# Risks And Limitations

- This audit is report-first. It identifies but does not fix stale
  `.aide/profile.yaml` focus or Harness `self-check` followup guidance.
- Q22 and Q23 target pilots were inspected read-only in sibling repos. This
  audit did not mutate or re-run write commands in Eureka or Dominium.
- Target-pilot evidence remains `needs_review` in the target repos.
- Eureka-specific and Dominium-specific golden tasks are not established.
- Q21 direct importer apply is broader than the real target-pilot allowed
  scopes; both pilots used manual manifest-guided imports after dry-run.
- The current committed export-pack manifest has stale/dirty source provenance
  relative to HEAD, and committed pack checksum validation fails on
  `manifest.yaml`; boundary validation still passes.
- Token estimates use chars / 4 only and do not prove exact tokenizer or
  provider billing savings.
- Review packets are local evidence packets, not live GPT/provider reviews.
- Adapter compiler outputs are advisory; this audit does not prove every target
  tool will read or obey them.
- Gateway/provider commands are report-only/metadata-only. This audit does not
  authorize runtime forwarding, provider calls, model calls, or network calls.
- Broad secret scans produced many policy/test/path matches. They were
  inspected as non-secret text; strict credential-shaped scans found no keys.
