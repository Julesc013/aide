# AIDE Advisory Model Registry

Q17 model files are route metadata only. They describe provider families,
capability dimensions, route profiles, hard floors, and fallback behavior so
`aide_lite.py route explain` can make deterministic advisory decisions before
any Gateway or provider integration exists.

No file in this directory contains provider credentials, live endpoint secrets,
model downloads, current pricing claims, or permission to call providers.

Every provider family in Q17 has `live_calls_allowed_in_q17: false`.
