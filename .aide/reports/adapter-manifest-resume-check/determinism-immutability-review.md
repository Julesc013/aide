# Determinism And Immutability Review

Repeated projection using the active Python interpreter produced identical bytes
for generated AdapterManifest reports and did not mutate source schema/helper
files.

The direct CLI command also reports `PASS_WITH_WARNINGS` and leaves no diff.

The nested Windows launcher form inside a Python subprocess produced a
non-blocking environment warning during probing; the direct required CLI command
and active-interpreter subprocess path both passed.
