# Superseding Main-Promotion Decision Packet

## Exact Candidate

- Target branch: `main`.
- Current target commit: `aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3`.
- Proposed source branch: `dev`.
- Proposed source commit: `d37219026462d5670f7a724980faf07e30abb85f`.
- Proposed source tree: `7637cc2ad1706a769457e262f90dcdbb0dce3c86`.
- Merge base: `aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3`.
- Candidate shape: five-commit fast-forward, no merge commit required.
- Complete diff: 117 files, 8,038 insertions, 72 deletions.
- Binary diff SHA-256:
  `c86168da9867f6e4988a18e7f524a5dbe7e1323895aad35cb5f7a3ce1597e463`.
- Ordered path-list SHA-256:
  `1f9eccbc03e3ffcc74370394c43c04fb9484de2a062ac0cbadd0309f9ec534fe`.

The hashes are over `git diff --binary origin/main..dev` and
`git diff --name-only origin/main..dev` respectively, with the refs above.

## Candidate Commits

1. `bfb86c12b9e6d2970024d29c57ba629994ec43cc` - accepted worker foundation ancestry synchronization.
2. `237ae8c49adce2b2e3232d83e6a3289fd9f4d6f3` - qualified control-plane documentation.
3. `be3a854abde73dd1d3498a20c240bd0c0a58c28b` - documentation integration closeout.
4. `4398497a1e43b77938636dcd0c7002d6ff045467` - exact repository Codex neutrality integration.
5. `d37219026462d5670f7a724980faf07e30abb85f` - neutrality integration closeout.

## Included And Excluded Scope

The candidate contains the qualified specification documentation, its bounded
queue/provenance closure, and the exact reviewed repository Codex neutrality
state. `.codex/config.toml` is absent and the five role TOMLs are
description-only.

It excludes the mixed broker implementation branch, isolated-host source,
GitHub target source, machine configuration, credentials, private archives,
tags, releases, and the 1,381 retained unknown-safety outputs.

## Validation State

- Active repository execution-setting scan: PASS; zero assignments.
- Five role TOMLs: PASS; description-only and parseable.
- Strict Codex startup: PASS; `codex-cli 0.145.0`.
- WorkUnit validation: PASS; 351 tasks and objects.
- Full AIDE validation: PASS against the final closeout tree.
- Changelog preview/validate/status: PASS, preview-only, publication false;
  four malformed historical commits are reported for review.
- `commit check --range origin/main..dev`: **FAIL**. The older published commit
  `bfb86c12` lacks an explicit PASS/WARN/FAIL/NOT RUN outcome in its Validation
  section. The other four candidate commits pass.

## Review State And Required Decision

This packet supersedes the historical `main -> be3a854a` subject. No approval
bound to that older target applies to this candidate.

The exact candidate is **not promotion-ready** while the required commit-range
check fails. Published history must not be rewritten merely to repair message
formatting. A reviewed policy-compliant disposition for `bfb86c12` is required,
followed by a fresh range check and the separate explicit human decision to
fast-forward `main` to this exact source commit.

No main mutation, tag, release, or publication action is authorized by this
packet or by the continuation prompt.
