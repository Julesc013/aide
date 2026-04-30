# Dominium Bridge Adoption

## Recommended Mode

Q07 recommends `pinned-managed-repo-layer`.

In this mode, Dominium later pins an AIDE commit, reviewed bundle, or future release artifact and consumes AIDE as a portable repo-native layer. The pin belongs to a future Dominium-side adoption task, not to Q07.

## Adoption Sequence

1. Review and accept Q07 in the AIDE repo.
2. Choose an AIDE pin in a future Dominium task.
3. Verify the AIDE pin with `py -3 scripts/aide validate`, `doctor`, `compile --dry-run`, and `migrate`.
4. Apply Dominium/XStack policy overlays in the Dominium repo only after a separate reviewed Dominium task authorizes it.
5. Generate or manage Dominium target files only after a later reviewed generated-output task permits those targets.

## Deferrals

- Q07 does not write to the Dominium repository.
- Q07 does not create Dominium generated files.
- Q07 does not define Dominium Runtime or product behavior.
- Q07 does not create a release bundle or package artifact.

## Review Gates

Dominium adoption requires review when:

- the AIDE pin changes;
- generated target policy changes;
- bridge compatibility or schema versions change;
- proof or audit requirements change;
- an external Dominium repo mutation is proposed.
