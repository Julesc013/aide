# AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01

Implement the first deterministic OKF-compatible AIDE knowledge bundle projection.

Build only:

- deterministic OKF-compatible markdown projection helper
- minimal frontmatter writer/parser/validator
- OKF bundle validation and lint
- thin `okf` CLI dispatch
- focused tests
- generated knowledge pages and reports
- queue evidence
- next-task prompt for independent check

The slice must not implement runtime behavior or make markdown/OKF pages execution, protocol, or evidence authority.

Expected result: `PASS_WITH_WARNINGS`, then stop at `needs_review`.

Recommended next task: `AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01`.
