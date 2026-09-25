# Validation intent and retained evidence

- PASS: accepted evaluation subject `b4501028`, tree `f90568b9`, and its
  independent evidence-only review SHA-256
  `711ecfe8c08e2ed3139d3caaa08ebc49e81ce7f904811b1978fc336798b53281`.
- PASS: the evaluation reviewer independently ran `pack-status`, `validate`,
  `doctor`, 31 lifecycle command-log checks and a two-commit structured range
  check on exact `b4501028`. That verdict explicitly withheld dev effect.
- PENDING: exact final integration candidate/tree, full base-to-candidate
  commit range, canonical candidate checks, archive hashes, independent
  integration-effect review and fresh pre-effect refs. Bind results in an
  external effect manifest before any ref mutation.
- NOT RUN: local dev fast-forward, normal push, main, tag or publication.
