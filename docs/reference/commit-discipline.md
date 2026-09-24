# Commit Discipline

Q27 defines AIDE's changelog-ready commit standard. New AIDE-managed queue work
uses:

```text
type(scope): summary
```

Subjects must be specific, 72 characters or fewer, and must not end with a
period. Substantive commits require these Markdown body sections:

- `## Summary`
- `## Why`
- `## Changed`
- `## Validation`
- `## Changelog`
- `## Risks`
- `## Follow-up`

Run:

```powershell
py -3 .aide/scripts/aide_lite.py commit check --latest
py -3 .aide/scripts/aide_lite.py commit check --range HEAD~5..HEAD
py -3 .aide/scripts/aide_lite.py commit check --range HEAD~5..HEAD --no-dispositions
py -3 .aide/scripts/aide_lite.py commit template
```

The optional hook is installed only when explicitly requested:

```powershell
py -3 .aide/scripts/aide_lite.py commit install-hook
```

Q27 does not rewrite old commits. Q34 reports malformed history and consumes
the structured body categories and AIDE trailers through `changelog preview`,
`changelog validate`, and `changelog status` to produce preview-only release
drafts.

## Exact Historical Dispositions

An immutable historical failure may be dispositioned only during a range
check and only through `.aide/git/commit-message-dispositions.json`. An
accepted record is bound to the full commit and tree object ids, ordered
parents, canonical message digest, exact checker failures, fixed narrow scope,
reviewer identity, review date, decision and evidence file digests, and a
digest of the record itself. Replacement objects are disabled while expanding
the range and reading commit messages.

Before any record can apply, the entire registry must be structurally valid
and have unique disposition and commit identities. Acceptance additionally
requires a content-hashed JSON decision whose exact disposition, commit, tree,
message, scope, decision, accountable reviewer, and date match the registry.
The reviewer must appear in the reviewed policy allowlist, and the date must
fall between the policy start and the current UTC date. A request for a
decision is not an acceptance decision.

Proposed, rejected, stale, incomplete, duplicate, wildcard, prefix, or
otherwise altered records have no effect. The original failed checks remain
visible under the `DISPOSITIONED` commit result, and the range result becomes
`PASS_WITH_DISPOSITIONS`; neither result claims the historical message passed.
Use `--no-dispositions` to reproduce raw range-policy failures. Latest-commit,
message-file, and hook checks never consume dispositions.

The general policy and schema are portable. This repository's decision
registry is source-specific and is excluded from exported packs so target
repositories cannot inherit AIDE's historical decisions.

## Portable Pack

Q31 and later pack exports include this policy, `.aide/hooks/commit-msg`,
`.aide/git/commit-template.md`, the commit checker commands, changelog preview
support, and the related reference docs through `aide-lite-pack-v0`. Imported
target repos receive the hook template but do not get `.git/hooks/commit-msg`;
hook installation remains an explicit target-repo operator action.
