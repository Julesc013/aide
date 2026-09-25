# Remaining risks and gates

- The two later update packs in the local canary are synthetic fixtures, not
  published predecessors. Semantic correctness of a project's chosen merge
  text remains its owner's decision.
- The local archive provenance independently binds bundled CLI bytes and
  checksums, while full integrated-tree and post-commit replay checks remain.
- Hostile process races, OS-level traffic isolation, native/hosted effects,
  published-byte download and stable-release support are separate gates.
- The combined artifact candidate still requires exact `dev` effect review
  and observed remote integration. No public release is claimed.
