# Inventory And Matrix Synchronization Checklist

Use this checklist when lane state, research posture, or inventory records change.

## Id Presence

- [ ] families, products, technologies, and versions referenced by manifests or matrices exist in inventory
- [ ] no candidate-family id is used as if it were a committed host family

## Posture Alignment

- [ ] `support-matrix.yaml` matches current support mode, tier, and state
- [ ] `capability-matrix.yaml` matches actual proven current capability and target capability
- [ ] `feature-coverage.yaml` matches required, optional, fallback, deferred, or unavailable posture
- [ ] `test-matrix.yaml` matches what was actually verified

## Candidate Versus Committed Separation

- [ ] backlog candidates remain in `inventory/legacy-ide-families.yaml`
- [ ] committed host families remain represented under `hosts/` and the canonical inventory files

## Blocked And Deferred Representation

- [ ] blocked lanes use explicit blocked posture where required
- [ ] deferred editor or workspace work is not confused with missing implementation
- [ ] matrix notes still explain major blockers or fallback boundaries
