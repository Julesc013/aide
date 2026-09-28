# Bounded request

Close the pause race at the existing Windows worker's suspended-child launch
boundary. Preserve intent/recovery and drain semantics, test with a synthetic
child, and retain separate Lite and release gates. Do not launch Codex.
