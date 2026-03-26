# AIDE Matrices

`matrices/` contains machine-readable posture data derived from inventory ids and canonical enums. These files describe support posture, capability posture, feature applicability, packaging posture, test posture, and platform reach.

## Matrix Roles

- `support-matrix.yaml`: target support tier, current support state, and support mode per family and technology lane.
- `capability-matrix.yaml`: current and target capability posture per family and technology lane.
- `feature-coverage.yaml`: seed feature-bucket applicability by lane.
- `packaging-matrix.yaml`: intended artifact class and packaging posture by technology.
- `test-matrix.yaml`: intended verification posture by lane.
- `platform-reach.yaml`: high-level host and target OS-family reach by lane.

## Inventory Consumption

Matrices consume ids from `inventory/` and enums from `inventory/enums.yaml`. They should reference canonical ids instead of restating prose policy.

## Partial Rows

Initial rows may be partial, placeholder-oriented, or conservative when research is incomplete. Unknowns should remain explicit rather than being guessed into false certainty.

## Expansion Rule

Future prompts should expand these matrices by adding researched rows, refining notes, and linking to exact-version inventory records without changing the overall shape unless a schema change is justified.
