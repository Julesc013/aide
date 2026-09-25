# Source validation

The first two-pack rollback regression failed before implementation because no rollback apply API existed. The final source candidate passed five rollback tests and two prior importer regressions; Python compilation, canonical `validate`, and diff whitespace checks passed. Exact commands, logs, hashes, and fixture limits are in `source-validation.md`.

Independent source review, combined-source tests, artifact generation, and extracted consumer qualification remain pending. This file records source tests only.
