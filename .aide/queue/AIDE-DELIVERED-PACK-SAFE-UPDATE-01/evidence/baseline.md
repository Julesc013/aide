# Baseline Characterization

- Source: `dev@a2ba43624bf99d3354a2a7429a3241e3967310fc`.
- `import-pack` validates pack checksums and installs absent safe-mode files.
- Existing target collisions are reported as conflicts from path and byte
  comparison only; no target-local ownership baseline is persisted.
- A later changed pack therefore cannot distinguish a safely updatable prior
  install from unknown ownership.
- Apply has no exact dry-run/apply plan identity and no durable interruption
  journal.
- The accepted DistributionApplyEngine remains fixture-only and explicitly
  reports real target apply as unimplemented.
