# AIDE Architecture Charters

## Purpose

This family defines focused architecture charters for the reboot model. Charters describe responsibility and boundaries; they do not claim implementation unless repository evidence supports it.

## Public Model

- [Core Charter](core-charter.md): AIDE Core as the durable semantic center.
- [Hosts Charter](hosts-charter.md): AIDE Hosts as shells and proof lanes.
- [Bridges Charter](bridges-charter.md): AIDE Bridges as bounded connection layers.

## Internal Core Split

- [Contract Charter](contract-charter.md)
- [Harness Charter](harness-charter.md)
- [Compatibility Charter](compatibility-charter.md)
- [Control Charter](control-charter.md)
- [SDK Charter](sdk-charter.md)

The Runtime charter is deferred until a queue item authorizes it. Q01 records Runtime as part of the Core split but does not create or implement runtime surfaces.

## Baseline Charter

- [Reboot Charter](reboot-charter.md): Q00 charter for the in-place reboot, first shipped stack, and non-goals.
