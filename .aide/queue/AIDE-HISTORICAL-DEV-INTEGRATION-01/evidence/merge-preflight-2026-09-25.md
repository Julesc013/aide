# Exact merge preflight

Base dev and observed remote dev:
`a5cd5ca5ddf7d0be561fbf2796b073b9f5d96fd2`.
Published historical evidence branch:
`7a2305f518940077892729b915734bb766a335e1`.
Merge base: `c6fdc754844cf7d42302218ce08307a7e05dcb61`.
The customization source candidate `8cad56c0` is in dev ancestry.

`git merge-tree --write-tree --messages` and the actual no-commit merge
showed the same substantive conflicts: queue index, DOCUMENTATION.md,
IMPLEMENT.md, and generated export/release paths. The combined source
`.aide/scripts/aide_lite.py` auto-merged. Generated paths were restored from
the current dev side pending regeneration from the committed combined source;
the older branch artifacts are retained only in history. No remote dev effect
has occurred in this integration branch yet.
