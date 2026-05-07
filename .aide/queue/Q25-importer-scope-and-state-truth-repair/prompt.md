# Prompt: Q25 Importer Scope And State Truth Repair

Repair the AIDE Lite Pack after QCHECK-02 found pack integrity, importer scope,
profile truth, and self-check guidance defects.

Required result:

- `pack-status` passes.
- Export pack checksum/provenance convention is coherent.
- `import-pack` defaults to target-safe scope and reports exact writes.
- Fixture import preserves manual `AGENTS.md` content and excludes broad source
  roots, source queue/history, generated context/reports, local state, secrets,
  raw prompts, and raw responses.
- `.aide/profile.yaml`, `scripts/aide self-check`, and
  `.aide/commands/catalog.yaml` reflect post-Q24/QCHECK truth.
- Q26 Eureka Pilot Review And Handover packet is generated.
- Q25 evidence is complete and Q25 stops at review.
